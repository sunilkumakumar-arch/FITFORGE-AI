import { BadRequestException } from '@nestjs/common';
import { PaymentsService } from './payments.service';

describe('PaymentsService', () => {
  it('rejects Razorpay webhooks with invalid signatures', async () => {
    const service = new PaymentsService({} as any, { get: (key: string) => key === 'RAZORPAY_WEBHOOK_SECRET' ? 'secret' : 'value' } as any, { log: jest.fn() } as any);
    await expect(service.handleWebhook('bad-signature', '{"event":"payment.captured"}', { event: 'payment.captured' })).rejects.toBeInstanceOf(BadRequestException);
  });
});
