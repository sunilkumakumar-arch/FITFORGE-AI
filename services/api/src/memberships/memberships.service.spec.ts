import { MembershipsService } from './memberships.service';

describe('MembershipsService', () => {
  it('renews from the current end date when membership is still active', async () => {
    const endDate = new Date('2026-07-01T00:00:00.000Z');
    const prisma: any = {
      membership: {
        findUnique: jest.fn().mockResolvedValue({ id: 'mem-1', organizationId: 'org-1', branchId: 'br-1', startDate: new Date('2026-06-01T00:00:00.000Z'), endDate, plan: { id: 'plan-1', durationDays: 30 } }),
        update: jest.fn().mockImplementation(({ data }) => Promise.resolve({ id: 'mem-1', organizationId: 'org-1', branchId: 'br-1', ...data })),
      },
    };
    const audit = { log: jest.fn() };
    const service = new MembershipsService(prisma, audit as any);
    const renewed = await service.renewMembership('mem-1', {}, 'actor-1');
    expect(renewed.status).toBe('active');
    expect(new Date(renewed.endDate).toISOString()).toBe('2026-07-31T00:00:00.000Z');
    expect(audit.log).toHaveBeenCalledWith(expect.objectContaining({ action: 'memberships.renew' }));
  });
});
