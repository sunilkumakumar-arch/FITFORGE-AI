import { BadRequestException } from '@nestjs/common';
import { CommerceService } from './commerce.service';

describe('CommerceService', () => {
  it('rejects checkout when stock is unavailable', async () => {
    const prisma: any = {
      $transaction: jest.fn((callback) => callback({ inventoryItem: { findFirst: jest.fn().mockResolvedValue({ quantityAvailable: 1, quantityReserved: 0 }) } })),
    };
    const service = new CommerceService(prisma, { log: jest.fn() } as any);
    jest.spyOn(service, 'getCart').mockResolvedValue({ id: 'cart-1', organizationId: 'org-1', branchId: 'br-1', userId: 'u-1', items: [{ productId: 'p-1', quantity: 2, unitPriceMinor: 100, product: { name: 'Whey' } }] } as any);
    await expect(service.checkout({ userId: 'u-1' })).rejects.toBeInstanceOf(BadRequestException);
  });
});
