import { WhatsappService } from './whatsapp.service';

describe('WhatsappService', () => {
  it('does not send templates to opted-out recipients', async () => {
    const prisma: any = {
      notificationPreference: { findUnique: jest.fn().mockResolvedValue({ enabled: false }) },
      notification: { create: jest.fn().mockResolvedValue({ id: 'not-1', status: 'failed' }) },
    };
    const service = new WhatsappService({ get: jest.fn() } as any, prisma);
    const result = await service.sendTemplate({ to: '919999999999', template: 'renewal_reminder' });
    expect(result.skipped).toBe(true);
    expect(prisma.notification.create).toHaveBeenCalledWith(expect.objectContaining({ data: expect.objectContaining({ status: 'failed' }) }));
  });
});
