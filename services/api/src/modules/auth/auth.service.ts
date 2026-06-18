import { ConflictException, Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcryptjs';
import { AuditService } from '../audit/audit.service';
import { AuthRepository } from './auth.repository';
import { LoginDto } from './dto/login.dto';
import { RefreshTokenDto } from './dto/refresh-token.dto';
import { RegisterDto } from './dto/register.dto';

@Injectable()
export class AuthService {
  constructor(
    private readonly authRepository: AuthRepository,
    private readonly jwtService: JwtService,
    private readonly config: ConfigService,
    private readonly audit: AuditService,
  ) {}

  async register(dto: RegisterDto) {
    const existing = await this.authRepository.findUserByEmail(dto.email);
    if (existing) {
      throw new ConflictException('Email already registered');
    }
    const rounds = Number(this.config.get('BCRYPT_ROUNDS') ?? 12);
    const passwordHash = await bcrypt.hash(dto.password, rounds);
    const user = await this.authRepository.createUserWithCredential({ ...dto, passwordHash });
    await this.audit.record({ action: 'auth.register', entityType: 'user', entityId: user.id, organizationId: dto.organizationId, branchId: dto.branchId });
    return this.issueTokens(user.id, dto.deviceId, dto.deviceName);
  }

  async login(dto: LoginDto) {
    const user = await this.authRepository.findUserByEmail(dto.email);
    if (!user?.credential) {
      throw new UnauthorizedException('Invalid credentials');
    }
    const valid = await bcrypt.compare(dto.password, user.credential.passwordHash);
    if (!valid) {
      throw new UnauthorizedException('Invalid credentials');
    }
    await this.audit.record({ action: 'auth.login', entityType: 'user', entityId: user.id, organizationId: user.organizationId });
    return this.issueTokens(user.id, dto.deviceId, dto.deviceName);
  }

  async refresh(dto: RefreshTokenDto) {
    try {
      const payload = await this.jwtService.verifyAsync<{ sub: string; sid: string }>(dto.refreshToken, {
        secret: this.config.get<string>('JWT_REFRESH_SECRET') ?? 'change-me-refresh-secret',
      });
      const session = await this.authRepository.findSession(payload.sid);
      if (!session || session.revokedAt) {
        throw new UnauthorizedException('Refresh token revoked');
      }
      const matches = await bcrypt.compare(dto.refreshToken, session.refreshTokenHash);
      if (!matches) {
        throw new UnauthorizedException('Invalid refresh token');
      }
      await this.authRepository.revokeSession(session.id);
      return this.issueTokens(payload.sub, session.deviceId, session.deviceName);
    } catch (error) {
      if (error instanceof UnauthorizedException) throw error;
      throw new UnauthorizedException('Invalid refresh token');
    }
  }

  async logout(dto: RefreshTokenDto) {
    const payload = await this.jwtService.verifyAsync<{ sid: string }>(dto.refreshToken, {
      secret: this.config.get<string>('JWT_REFRESH_SECRET') ?? 'change-me-refresh-secret',
    });
    await this.authRepository.revokeSession(payload.sid);
    return { success: true };
  }

  async me(userId: string) {
    const user = await this.authRepository.findUserById(userId);
    if (!user) {
      throw new UnauthorizedException('User not found');
    }
    const { credential: _credential, ...safeUser } = user as any;
    return safeUser;
  }

  private async issueTokens(userId: string, deviceId?: string | null, deviceName?: string | null) {
    const user = await this.authRepository.findUserById(userId);
    if (!user) {
      throw new UnauthorizedException('User not found');
    }
    const permissions = this.extractPermissions(user);
    const roleKeys = this.extractRoleKeys(user);
    const branchIds = (user.branchAccess ?? []).map((access: any) => access.branchId);
    const accessPayload = { sub: user.id, email: user.email, organizationId: user.organizationId, branchIds, roleKeys, permissions };
    const accessToken = await this.jwtService.signAsync(accessPayload, {
      secret: this.config.get<string>('JWT_ACCESS_SECRET') ?? 'change-me-access-secret',
      expiresIn: (this.config.get<string>('JWT_ACCESS_EXPIRES_IN') ?? '15m') as any,
    });
    const session = await this.authRepository.createSession({
      userId: user.id,
      refreshTokenHash: 'pending',
      deviceId,
      deviceName,
      expiresAt: this.refreshExpiry(),
    });
    const refreshToken = await this.jwtService.signAsync({ sub: user.id, sid: session.id }, {
      secret: this.config.get<string>('JWT_REFRESH_SECRET') ?? 'change-me-refresh-secret',
      expiresIn: (this.config.get<string>('JWT_REFRESH_EXPIRES_IN') ?? '30d') as any,
    });
    const refreshTokenHash = await bcrypt.hash(refreshToken, Number(this.config.get('BCRYPT_ROUNDS') ?? 12));
    await (this.authRepository as any).prisma.userSession.update({ where: { id: session.id }, data: { refreshTokenHash } });
    return { accessToken, refreshToken, tokenType: 'Bearer', expiresIn: this.config.get<string>('JWT_ACCESS_EXPIRES_IN') ?? '15m' };
  }

  private extractPermissions(user: any): string[] {
    return [...new Set<string>((user.roles ?? []).flatMap((assignment: any) => assignment.role.permissions.map((item: any) => String(item.permission.key))))];
  }

  private extractRoleKeys(user: any): string[] {
    return [...new Set<string>((user.roles ?? []).map((assignment: any) => String(assignment.role.systemKey ?? assignment.role.name)))];
  }

  private refreshExpiry(): Date {
    const raw = this.config.get<string>('JWT_REFRESH_EXPIRES_IN') ?? '30d';
    const days = raw.endsWith('d') ? Number(raw.replace('d', '')) : 30;
    return new Date(Date.now() + days * 24 * 60 * 60 * 1000);
  }
}
