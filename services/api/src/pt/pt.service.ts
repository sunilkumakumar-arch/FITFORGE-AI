import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { AuditService } from '../core/audit.service';
import { PrismaService } from '../core/prisma.service';
import { ConsumePtCreditDto, CreatePtPackageDto, PurchasePtPackageDto } from './dto/pt.dto';

@Injectable()
export class PtService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}
  createPackage(dto: CreatePtPackageDto) { return (this.prisma as any).ptPackage.create({ data: { ...dto, currency: dto.currency ?? 'INR' } }); }
  listPackages(query: any) { return (this.prisma as any).ptPackage.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), isActive: true }, orderBy: { createdAt: 'desc' } }); }
  async purchasePackage(dto: PurchasePtPackageDto, actorUserId?: string) {
    const pkg = await (this.prisma as any).ptPackage.findUnique({ where: { id: dto.packageId } });
    if (!pkg?.isActive) throw new NotFoundException('Active PT package not found');
    const payment = await (this.prisma as any).payment.findUnique({ where: { id: dto.paymentId } });
    if (!payment || payment.status !== 'paid') throw new BadRequestException('Paid payment is required to activate PT credits');
    const entry = await (this.prisma as any).ptCreditLedger.create({ data: { organizationId: pkg.organizationId, branchId: pkg.branchId, memberId: dto.memberId, trainerId: dto.trainerId, packageId: pkg.id, paymentId: dto.paymentId, creditsDelta: pkg.sessionCredits, reason: 'package_purchase', expiresAt: new Date(Date.now() + pkg.validityDays * 24 * 60 * 60 * 1000) } });
    await this.audit.log({ action: 'pt.package_purchase', entityType: 'ptCreditLedger', entityId: entry.id, actorUserId, organizationId: entry.organizationId, branchId: entry.branchId, afterData: entry });
    return entry;
  }
  async consumeCredit(dto: ConsumePtCreditDto, actorUserId?: string) {
    const balance = await this.balance(dto.memberId, dto.trainerId);
    if (balance.availableCredits < 1) throw new BadRequestException('No PT credits available');
    const source = await (this.prisma as any).ptCreditLedger.findFirst({ where: { memberId: dto.memberId, ...(dto.trainerId ? { trainerId: dto.trainerId } : {}), creditsDelta: { gt: 0 }, OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }] }, orderBy: { expiresAt: 'asc' } });
    const entry = await (this.prisma as any).ptCreditLedger.create({ data: { organizationId: source.organizationId, branchId: source.branchId, memberId: dto.memberId, trainerId: dto.trainerId, packageId: source.packageId, bookingId: dto.bookingId, creditsDelta: -1, reason: 'booking_completed' } });
    await (this.prisma as any).trainerBooking.update({ where: { id: dto.bookingId }, data: { status: 'completed' } }).catch(() => undefined);
    await this.audit.log({ action: 'pt.credit_consume', entityType: 'ptCreditLedger', entityId: entry.id, actorUserId, organizationId: entry.organizationId, branchId: entry.branchId, afterData: entry });
    return entry;
  }
  async balance(memberId: string, trainerId?: string) { const entries = await (this.prisma as any).ptCreditLedger.findMany({ where: { memberId, ...(trainerId ? { trainerId } : {}), OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }] } }); return { memberId, trainerId, availableCredits: entries.reduce((sum: number, entry: any) => sum + entry.creditsDelta, 0) }; }
}
