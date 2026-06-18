import { JobsService } from './jobs.service';

describe('JobsService', () => {
  it('releases expired reservations and decrements reserved stock', async () => {
    const tx = { inventoryItem: { update: jest.fn() }, inventoryReservation: { update: jest.fn() } };
    const prisma: any = {
      systemJobRun: { create: jest.fn().mockResolvedValue({ id: 'job-1' }), update: jest.fn().mockImplementation(({ data }) => Promise.resolve(data)) },
      inventoryReservation: { findMany: jest.fn().mockResolvedValue([{ id: 'res-1', inventoryItemId: 'inv-1', quantity: 2 }]) },
      $transaction: jest.fn((callback) => callback(tx)),
    };
    const service = new JobsService(prisma, {} as any, {} as any);
    const result = await service.releaseExpiredReservations();
    expect(result.status).toBe('succeeded');
    expect(result.summary).toEqual({ released: 1 });
    expect(tx.inventoryItem.update).toHaveBeenCalledWith({ where: { id: 'inv-1' }, data: { quantityReserved: { decrement: 2 } } });
  });

  it('aggregates branch metrics', async () => {
    const prisma: any = {
      systemJobRun: { create: jest.fn().mockResolvedValue({ id: 'job-1' }), update: jest.fn().mockImplementation(({ data }) => Promise.resolve(data)) },
      branch: { findMany: jest.fn().mockResolvedValue([{ id: 'br-1', organizationId: 'org-1' }]) },
      membership: { count: jest.fn().mockResolvedValue(3) },
      attendanceLog: { count: jest.fn().mockResolvedValue(5) },
      payment: { count: jest.fn().mockResolvedValue(2), findMany: jest.fn().mockResolvedValue([{ amountMinor: 100 }, { amountMinor: 200 }]) },
      order: { count: jest.fn().mockResolvedValue(4) },
      dailyBranchMetric: { upsert: jest.fn() },
    };
    const service = new JobsService(prisma, {} as any, {} as any);
    const result = await service.aggregateDailyBranchMetrics(new Date('2026-06-18T12:00:00.000Z'));
    expect(result.status).toBe('succeeded');
    expect(result.summary).toMatchObject({ upserted: 1 });
    expect(prisma.dailyBranchMetric.upsert).toHaveBeenCalled();
  });
});
