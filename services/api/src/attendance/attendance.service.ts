import { BadRequestException, Injectable } from '@nestjs/common';
import { createHash, randomBytes } from 'crypto';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';

@Injectable()
export class AttendanceService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}
  async createQrToken(branchId: string, ttlSeconds = 300) {
    const rawToken = randomBytes(32).toString('hex');
    const tokenHash = this.hash(rawToken);
    const expiresAt = new Date(Date.now() + ttlSeconds * 1000);
    const record = await (this.prisma as any).qrAttendanceToken.create({ data: { branchId, tokenHash, expiresAt } });
    return { token: rawToken, qrPayload: JSON.stringify({ branchId, token: rawToken }), expiresAt: record.expiresAt };
  }
  async qrCheckIn(dto: any, actorUserId?: string) {
    const token = await (this.prisma as any).qrAttendanceToken.findUnique({ where: { tokenHash: this.hash(dto.token) }, include: { branch: true } });
    if (!token || token.expiresAt < new Date() || token.branchId !== dto.branchId) throw new BadRequestException('Invalid or expired QR token');
    const membership = await (this.prisma as any).membership.findFirst({ where: { memberId: dto.memberId, branchId: dto.branchId, status: 'active', endDate: { gte: new Date() } } });
    if (!membership) throw new BadRequestException('Active membership required for check-in');
    const log = await (this.prisma as any).attendanceLog.create({ data: { organizationId: token.branch.organizationId, branchId: dto.branchId, memberId: dto.memberId, method: 'qr', metadata: { source: 'qr', deviceId: dto.deviceId } } });
    await this.audit.log({ action: 'attendance.qr_check_in', entityType: 'attendanceLog', entityId: log.id, actorUserId, organizationId: log.organizationId, branchId: log.branchId });
    return log;
  }
  checkOut(id: string) { return (this.prisma as any).attendanceLog.update({ where: { id }, data: { checkOutAt: new Date() } }); }
  private hash(value: string) { return createHash('sha256').update(value).digest('hex'); }
}
