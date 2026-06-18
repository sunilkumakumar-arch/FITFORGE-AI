import { BadRequestException, Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { createHmac } from 'crypto';
import Razorpay from 'razorpay';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';

@Injectable()
export class PaymentsService {
  private readonly razorpay: Razorpay;
  constructor(private readonly prisma: PrismaService, private readonly config: ConfigService, private readonly audit: AuditService) {
    this.razorpay = new Razorpay({ key_id: config.get<string>('RAZORPAY_KEY_ID') ?? 'rzp_test_key', key_secret: config.get<string>('RAZORPAY_KEY_SECRET') ?? 'rzp_test_secret' });
  }
  async createRazorpayOrder(dto: any) {
    const receipt = dto.idempotencyKey ?? `ff_${Date.now()}`;
    const order = await this.razorpay.orders.create({ amount: dto.amountMinor, currency: dto.currency ?? 'INR', receipt, notes: { purpose: dto.purpose } });
    const payment = await (this.prisma as any).payment.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, orderId: dto.orderId, purpose: dto.purpose, amountMinor: dto.amountMinor, currency: dto.currency ?? 'INR', idempotencyKey: receipt, providerOrderId: order.id, metadata: { razorpayOrder: order } } });
    return { paymentId: payment.id, providerOrderId: order.id, amount: order.amount, currency: order.currency, keyId: this.config.get<string>('RAZORPAY_KEY_ID') };
  }
  async handleWebhook(signature: string, rawBody: string, event: any) {
    const expected = createHmac('sha256', this.config.get<string>('RAZORPAY_WEBHOOK_SECRET') ?? 'change-me-webhook').update(rawBody).digest('hex');
    if (signature !== expected) throw new BadRequestException('Invalid Razorpay signature');
    const entity = event.payload?.payment?.entity;
    if (event.event === 'payment.captured' && entity?.order_id) {
      const payment = await (this.prisma as any).payment.updateMany({ where: { providerOrderId: entity.order_id }, data: { status: 'paid', providerPaymentId: entity.id, metadata: event } });
      await this.audit.log({ action: 'payments.razorpay_webhook_paid', entityType: 'payment', entityId: entity.id, afterData: event });
      return { processed: true, updated: payment.count };
    }
    return { processed: true, ignored: event.event };
  }
}
