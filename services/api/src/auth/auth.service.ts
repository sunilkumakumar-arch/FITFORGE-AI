import { ConflictException, Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcryptjs';
import { createHash, randomBytes } from 'crypto';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';

@Injectable()
export class AuthService {
  constructor(private readonly prisma: PrismaService, private readonly jwt: JwtService, private readonly config: ConfigService, private readonly audit: AuditService) {}

  async register(dto: any) {
    if (await (this.prisma as any).user.findUnique({ where: { email: dto.email } })) throw new ConflictException('Email already exists');
    const passwordHash = await bcrypt.hash(dto.password, 12);
    const user = await (this.prisma as any).user.create({ data: { email: dto.email, firstName: dto.firstName, lastName: dto.lastName, phone: dto.phone, organizationId: dto.organizationId, credential: { create: { passwordHash } } } });
    await this.audit.log({ action: 'auth.register', entityType: 'user', entityId: user.id, organizationId: user.organizationId });
    return this.issueTokens(user.id, dto.deviceId);
  }

  async login(dto: any) {
    const user = await (this.prisma as any).user.findUnique({ where: { email: dto.email }, include: { credential: true } });
    if (!user?.credential || !(await bcrypt.compare(dto.password, user.credential.passwordHash))) throw new UnauthorizedException('Invalid credentials');
    await this.audit.log({ action: 'auth.login', entityType: 'user', entityId: user.id, organizationId: user.organizationId });
    return this.issueTokens(user.id, dto.deviceId);
  }

  async refresh(refreshToken: string) {
    const payload = await this.jwt.verifyAsync(refreshToken, { secret: this.config.get<string>('JWT_REFRESH_SECRET') ?? 'change-me-refresh' });
    const session = await (this.prisma as any).refreshSession.findUnique({ where: { id: payload.sid } });
    if (!session || session.revokedAt || !(await bcrypt.compare(refreshToken, session.refreshTokenHash))) throw new UnauthorizedException('Invalid refresh token');
    await (this.prisma as any).refreshSession.update({ where: { id: session.id }, data: { revokedAt: new Date() } });
    return this.issueTokens(payload.sub, session.deviceId);
  }

  async me(userId: string) { return (this.prisma as any).user.findUnique({ where: { id: userId }, include: { roles: { include: { role: true } }, memberships: true } }); }

  async requestPasswordReset(email: string) {
    const user = await (this.prisma as any).user.findUnique({ where: { email } });
    if (!user) return { success: true };
    const token = randomBytes(32).toString('hex');
    await (this.prisma as any).passwordResetToken.create({ data: { userId: user.id, tokenHash: this.hash(token), expiresAt: new Date(Date.now() + 15 * 60 * 1000) } });
    await this.audit.log({ action: 'auth.password_reset_request', entityType: 'user', entityId: user.id, organizationId: user.organizationId });
    return { success: true, resetToken: token };
  }

  async resetPassword(token: string, password: string) {
    const reset = await (this.prisma as any).passwordResetToken.findUnique({ where: { tokenHash: this.hash(token) }, include: { user: true } });
    if (!reset || reset.usedAt || reset.expiresAt < new Date()) throw new UnauthorizedException('Invalid or expired reset token');
    const passwordHash = await bcrypt.hash(password, 12);
    await (this.prisma as any).$transaction(async (tx: any) => {
      await tx.userCredential.upsert({ where: { userId: reset.userId }, create: { userId: reset.userId, passwordHash }, update: { passwordHash } });
      await tx.passwordResetToken.update({ where: { id: reset.id }, data: { usedAt: new Date() } });
      await tx.refreshSession.updateMany({ where: { userId: reset.userId, revokedAt: null }, data: { revokedAt: new Date() } });
    });
    await this.audit.log({ action: 'auth.password_reset_complete', entityType: 'user', entityId: reset.userId, organizationId: reset.user.organizationId });
    return { success: true };
  }

  private async issueTokens(userId: string, deviceId?: string) {
    const user = await (this.prisma as any).user.findUnique({ where: { id: userId }, include: { roles: { include: { role: { include: { permissions: { include: { permission: true } } } } } } } });
    const roles = (user.roles ?? []).map((r: any) => r.role.key);
    const permissions = [...new Set<string>((user.roles ?? []).flatMap((r: any) => r.role.permissions.map((p: any) => p.permission.key)))];
    const accessPayload = { sub: user.id, email: user.email, organizationId: user.organizationId, roles, permissions, branchIds: (user.roles ?? []).map((r: any) => r.branchId).filter(Boolean) };
    const accessToken = await this.jwt.signAsync(accessPayload, { secret: this.config.get<string>('JWT_ACCESS_SECRET') ?? 'change-me-access', expiresIn: (this.config.get<string>('JWT_ACCESS_EXPIRES_IN') ?? '15m') as any });
    const session = await (this.prisma as any).refreshSession.create({ data: { userId: user.id, refreshTokenHash: 'pending', deviceId, expiresAt: new Date(Date.now() + 30 * 86400_000) } });
    const refreshToken = await this.jwt.signAsync({ sub: user.id, sid: session.id }, { secret: this.config.get<string>('JWT_REFRESH_SECRET') ?? 'change-me-refresh', expiresIn: (this.config.get<string>('JWT_REFRESH_EXPIRES_IN') ?? '30d') as any });
    await (this.prisma as any).refreshSession.update({ where: { id: session.id }, data: { refreshTokenHash: await bcrypt.hash(refreshToken, 12) } });
    return { accessToken, refreshToken, tokenType: 'Bearer' };
  }

  private hash(value: string) {
    return createHash('sha256').update(value).digest('hex');
  }
}
