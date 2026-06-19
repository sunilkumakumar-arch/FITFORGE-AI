import { BadRequestException, Injectable } from '@nestjs/common';
import { createHash, randomBytes } from 'crypto';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';
import { CreateQrTokenDto, ManualCheckInDto, QrCheckInDto } from './dto/attendance.dto';

@Injectable()
export class AttendanceService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}

  async createQrToken(dtoOrBranchId: CreateQrTokenDto | string, ttlSeconds = 300) {
    const branchId = typeof dtoOrBranchId === 'string' ? dtoOrBranchId : dtoOrBranchId.branchId;
    const tokenTtl = typeof dtoOrBranchId === 'string' ? ttlSeconds : (dtoOrBranchId.ttlSeconds ?? 300);
    const branch = await (this.prisma as any).branch.findUnique({ where: { id: branchId } });
    if (!branch) throw new BadRequestException('Branch not found');
    const rawToken = randomBytes(32).toString('hex');
    const tokenHash = this.hash(rawToken);
    const expiresAt = new Date(Date.now() + tokenTtl * 1000);
    const record = await (this.prisma as any).qrAttendanceToken.create({ data: { branchId, tokenHash, expiresAt } });
    return { token: rawToken, qrPayload: JSON.stringify({ branchId, token: rawToken, expiresAt: record.expiresAt }), expiresAt: record.expiresAt };
  }

  async qrCheckIn(dto: QrCheckInDto, actorUserId?: string) {
    const token = await (this.prisma as any).qrAttendanceToken.findUnique({ where: { tokenHash: this.hash(dto.token) }, include: { branch: true } });
    if (!token || token.expiresAt < new Date() || token.branchId !== dto.branchId) throw new BadRequestException('Invalid or expired QR token');
    const membership = await (this.prisma as any).membership.findFirst({ where: { memberId: dto.memberId, branchId: dto.branchId, status: 'active', endDate: { gte: new Date() } } });
    if (!membership) throw new BadRequestException('Active membership required for check-in');
    await this.ensureNoDuplicateCheckIn(dto.memberId, dto.branchId);
    const log = await (this.prisma as any).attendanceLog.create({ data: { organizationId: token.branch.organizationId, branchId: dto.branchId, memberId: dto.memberId, method: 'qr', metadata: { source: 'qr', deviceId: dto.deviceId } } });
    await this.audit.log({ action: 'attendance.qr_check_in', entityType: 'attendanceLog', entityId: log.id, actorUserId, organizationId: log.organizationId, branchId: log.branchId });
    return log;
  }

  async manualCheckIn(dto: ManualCheckInDto, actorUserId?: string) {
    await this.ensureNoDuplicateCheckIn(dto.memberId, dto.branchId);
    const log = await (this.prisma as any).attendanceLog.create({
      data: {
        organizationId: dto.organizationId,
        branchId: dto.branchId,
        memberId: dto.memberId,
        method: dto.method ?? 'manual',
        metadata: { source: dto.method ?? 'manual', deviceId: dto.deviceId },
      },
    });
    await this.audit.log({ action: 'attendance.manual_check_in', entityType: 'attendanceLog', entityId: log.id, actorUserId, organizationId: log.organizationId, branchId: log.branchId });
    return log;
  }

  checkOut(id: string) { return (this.prisma as any).attendanceLog.update({ where: { id }, data: { checkOutAt: new Date() } }); }

  list(query: any) {
    return (this.prisma as any).attendanceLog.findMany({
      where: {
        ...(query.organizationId ? { organizationId: query.organizationId } : {}),
        ...(query.branchId ? { branchId: query.branchId } : {}),
        ...(query.memberId ? { memberId: query.memberId } : {}),
      },
      orderBy: { checkInAt: 'desc' },
    });
  }

  private async ensureNoDuplicateCheckIn(memberId: string, branchId: string) {
    const windowStart = new Date(Date.now() - 5 * 60 * 1000);
    const duplicate = await (this.prisma as any).attendanceLog.findFirst({
      where: { memberId, branchId, checkInAt: { gte: windowStart }, checkOutAt: null },
    });
    if (duplicate) throw new BadRequestException('Member already checked in recently');
  }

  private hash(value: string) { return createHash('sha256').update(value).digest('hex'); }
}
