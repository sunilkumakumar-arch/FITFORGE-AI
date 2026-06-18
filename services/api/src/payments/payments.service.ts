import { BadRequestException, Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { createHmac } from 'crypto';
import Razorpay from 'razorpay';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';
import { CreateRazorpayOrderDto, RefundPaymentDto } from './dto/payments.dto';

@Injectable()
export class PaymentsService {
  private readonly razorpay: Razorpay;
  constructor(private readonly prisma: PrismaService, private readonly config: ConfigService, private readonly audit: AuditService) {
    this.razorpay = new Razorpay({ key_id: config.get<string>('RAZORPAY_KEY_ID') ?? 'rzp_test_key', key_secret: config.get<string>('RAZORPAY_KEY_SECRET') ?? 'rzp_test_secret' });
  }
  async createRazorpayOrder(dto: CreateRazorpayOrderDto) {
    const existing = await (this.prisma as any).payment.findUnique({ where: { organizationId_idempotencyKey: { organizationId: dto.organizationId, idempotencyKey: dto.idempotencyKey } } }).catch(() => null);
    if (existing) return { paymentId: existing.id, providerOrderId: existing.providerOrderId, amount: existing.amountMinor, currency: existing.currency, keyId: this.config.get<string>('RAZORPAY_KEY_ID'), reused: true };
    const receipt = dto.idempotencyKey;
    const order = await this.razorpay.orders.create({ amount: dto.amountMinor, currency: dto.currency ?? 'INR', receipt, notes: { purpose: dto.purpose } });
    const payment = await (this.prisma as any).payment.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, orderId: dto.orderId, purpose: dto.purpose, amountMinor: dto.amountMinor, currency: dto.currency ?? 'INR', idempotencyKey: receipt, providerOrderId: order.id, metadata: { ...(dto.metadata ?? {}), razorpayOrder: order } } });
    await this.audit.log({ action: 'payments.razorpay_order_create', entityType: 'payment', entityId: payment.id, organizationId: payment.organizationId, branchId: payment.branchId, afterData: payment });
    return { paymentId: payment.id, providerOrderId: order.id, amount: order.amount, currency: order.currency, keyId: this.config.get<string>('RAZORPAY_KEY_ID') };
  }

  async handleWebhook(signature: string, rawBody: string, event: any) {
    const expected = createHmac('sha256', this.config.get<string>('RAZORPAY_WEBHOOK_SECRET') ?? 'change-me-webhook').update(rawBody).digest('hex');
    if (signature !== expected) throw new BadRequestException('Invalid Razorpay signature');
    const eventId = event.id ?? `${event.event}:${event.payload?.payment?.entity?.id ?? event.created_at ?? Date.now()}`;
    const existing = await (this.prisma as any).paymentWebhookEvent.findUnique({ where: { eventId } }).catch(() => null);
    if (existing?.processedAt) return { processed: true, duplicate: true };
    await (this.prisma as any).paymentWebhookEvent.upsert({
      where: { eventId },
      create: { provider: 'razorpay', eventId, eventType: event.event, payload: event },
      update: { payload: event },
    });
    const entity = event.payload?.payment?.entity;
    if (event.event === 'payment.captured' && entity?.order_id) {
      const payment = await (this.prisma as any).payment.updateMany({ where: { providerOrderId: entity.order_id }, data: { status: 'paid', providerPaymentId: entity.id, metadata: event } });
      await (this.prisma as any).paymentWebhookEvent.update({ where: { eventId }, data: { processedAt: new Date() } });
      await this.audit.log({ action: 'payments.razorpay_webhook_paid', entityType: 'payment', entityId: entity.id, afterData: event });
      return { processed: true, updated: payment.count };
    }
    await (this.prisma as any).paymentWebhookEvent.update({ where: { eventId }, data: { processedAt: new Date() } });
    return { processed: true, ignored: event.event };
  }

  async refundPayment(paymentId: string, dto: RefundPaymentDto) {
    const payment = await (this.prisma as any).payment.findUnique({ where: { id: paymentId } });
    if (!payment?.providerPaymentId) throw new BadRequestException('Captured provider payment is required for refund');
    const refund = await this.razorpay.payments.refund(payment.providerPaymentId, { amount: dto.amountMinor, notes: { reason: dto.reason ?? 'requested_by_admin' } } as any);
    const updated = await (this.prisma as any).payment.update({ where: { id: paymentId }, data: { status: dto.amountMinor >= payment.amountMinor ? 'refunded' : 'paid', metadata: { ...(payment.metadata ?? {}), refund } } });
    await this.audit.log({ action: 'payments.refund', entityType: 'payment', entityId: paymentId, organizationId: payment.organizationId, branchId: payment.branchId, beforeData: payment, afterData: updated });
    return { payment: updated, refund };
  }

  list(query: any) {
    return (this.prisma as any).payment.findMany({
      where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), ...(query.status ? { status: query.status } : {}) },
      orderBy: { createdAt: 'desc' },
    });
  }
}
