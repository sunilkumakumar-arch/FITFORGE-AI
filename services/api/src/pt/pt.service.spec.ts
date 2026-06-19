import { BadRequestException } from '@nestjs/common';
import { PtService } from './pt.service';

describe('PtService', () => {
  it('requires a paid payment before activating package credits', async () => {
    const prisma: any = { ptPackage: { findUnique: jest.fn().mockResolvedValue({ id: 'pkg-1', isActive: true }) }, payment: { findUnique: jest.fn().mockResolvedValue({ status: 'pending' }) } };
    const service = new PtService(prisma, { log: jest.fn() } as any);
    await expect(service.purchasePackage({ memberId: 'mem-1', packageId: 'pkg-1', paymentId: 'pay-1' })).rejects.toBeInstanceOf(BadRequestException);
  });

  it('computes available PT credit balance', async () => {
    const prisma: any = { ptCreditLedger: { findMany: jest.fn().mockResolvedValue([{ creditsDelta: 5 }, { creditsDelta: -1 }]) } };
    const service = new PtService(prisma, { log: jest.fn() } as any);
    await expect(service.balance('mem-1')).resolves.toMatchObject({ availableCredits: 4 });
  });
});
