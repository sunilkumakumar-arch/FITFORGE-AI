import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../core/prisma.service';
import { PaymentsService } from '../payments/payments.service';

@Injectable()
export class JobsService {
  constructor(private readonly prisma: PrismaService, private readonly config: ConfigService, private readonly payments: PaymentsService) {}

  async releaseExpiredReservations() {
    return this.runJob('inventory.release_expired_reservations', async () => {
      const expired = await (this.prisma as any).inventoryReservation.findMany({ where: { status: 'active', expiresAt: { lt: new Date() } } });
      for (const reservation of expired) {
        await (this.prisma as any).$transaction(async (tx: any) => {
          await tx.inventoryItem.update({ where: { id: reservation.inventoryItemId }, data: { quantityReserved: { decrement: reservation.quantity } } });
          await tx.inventoryReservation.update({ where: { id: reservation.id }, data: { status: 'released', releasedAt: new Date() } });
        });
      }
      return { released: expired.length };
    });
  }

  async scanMembershipRenewals(daysAhead = 7) {
    return this.runJob('memberships.scan_auto_renewals', async () => {
      const until = new Date(Date.now() + daysAhead * 24 * 60 * 60 * 1000);
      const memberships = await (this.prisma as any).membership.findMany({ where: { autoRenew: true, status: 'active', endDate: { lte: until } }, include: { plan: true } });
      let createdPayments = 0;
      for (const membership of memberships) {
        const existing = await (this.prisma as any).payment.findFirst({ where: { organizationId: membership.organizationId, purpose: 'membership_renewal', status: 'pending', metadata: { path: ['membershipId'], equals: membership.id } } }).catch(() => null);
        if (existing) continue;
        await (this.prisma as any).payment.create({ data: { organizationId: membership.organizationId, branchId: membership.branchId, purpose: 'membership_renewal', amountMinor: membership.plan.priceMinor, currency: membership.plan.currency, idempotencyKey: `renewal-${membership.id}-${membership.endDate.toISOString().slice(0,10)}`, metadata: { membershipId: membership.id, planId: membership.planId } } });
        createdPayments++;
      }
      return { scanned: memberships.length, createdPayments };
    });
  }

  async reconcileRazorpayPayments() {
    return this.runJob('payments.razorpay_reconcile_pending', async () => {
      const pending = await (this.prisma as any).payment.findMany({ where: { provider: 'razorpay', status: 'pending', providerOrderId: { not: null } }, take: 50 });
      let reconciled = 0;
      for (const payment of pending) {
        const orderPayments = await (this.payments as any).razorpay.orders.fetchPayments(payment.providerOrderId).catch(() => null);
        const captured = orderPayments?.items?.find((item: any) => item.status === 'captured');
        if (!captured) continue;
        await (this.prisma as any).payment.update({ where: { id: payment.id }, data: { status: 'paid', providerPaymentId: captured.id, metadata: { ...(payment.metadata ?? {}), reconciliation: captured } } });
        reconciled++;
      }
      return { scanned: pending.length, reconciled };
    });
  }

  async aggregateDailyBranchMetrics(date = new Date()) {
    return this.runJob('analytics.aggregate_daily_branch_metrics', async () => {
      const metricDate = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
      const nextDate = new Date(metricDate.getTime() + 24 * 60 * 60 * 1000);
      const branches = await (this.prisma as any).branch.findMany();
      let upserted = 0;
      for (const branch of branches) {
        const [activeMemberships, attendanceCount, paidPayments, orders, payments] = await Promise.all([
          (this.prisma as any).membership.count({ where: { branchId: branch.id, status: 'active' } }),
          (this.prisma as any).attendanceLog.count({ where: { branchId: branch.id, checkInAt: { gte: metricDate, lt: nextDate } } }),
          (this.prisma as any).payment.count({ where: { branchId: branch.id, status: 'paid', createdAt: { gte: metricDate, lt: nextDate } } }),
          (this.prisma as any).order.count({ where: { branchId: branch.id, createdAt: { gte: metricDate, lt: nextDate } } }),
          (this.prisma as any).payment.findMany({ where: { branchId: branch.id, status: 'paid', createdAt: { gte: metricDate, lt: nextDate } } }),
        ]);
        const revenueMinor = payments.reduce((sum: number, payment: any) => sum + payment.amountMinor, 0);
        await (this.prisma as any).dailyBranchMetric.upsert({ where: { branchId_metricDate: { branchId: branch.id, metricDate } }, create: { organizationId: branch.organizationId, branchId: branch.id, metricDate, activeMemberships, attendanceCount, paidPayments, revenueMinor, ordersCount: orders }, update: { activeMemberships, attendanceCount, paidPayments, revenueMinor, ordersCount: orders } });
        upserted++;
      }
      return { metricDate, upserted };
    });
  }

  private async runJob(jobName: string, callback: () => Promise<Record<string, unknown>>) {
    const run = await (this.prisma as any).systemJobRun.create({ data: { jobName, status: 'running' } });
    try {
      const summary = await callback();
      return (this.prisma as any).systemJobRun.update({ where: { id: run.id }, data: { status: 'succeeded', completedAt: new Date(), summary } });
    } catch (error) {
      return (this.prisma as any).systemJobRun.update({ where: { id: run.id }, data: { status: 'failed', completedAt: new Date(), summary: { error: error instanceof Error ? error.message : String(error) } } });
    }
  }
}
