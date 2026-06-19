import { BadRequestException } from '@nestjs/common';
import { TrainersService } from './trainers.service';

describe('TrainersService', () => {
  it('rejects booking when trainer already has a conflicting session', async () => {
    const prisma: any = { trainerAvailability: { findFirst: jest.fn().mockResolvedValue({ id: 'av-1' }) }, trainerBooking: { findFirst: jest.fn().mockResolvedValue({ id: 'bk-1' }), create: jest.fn() } };
    const service = new TrainersService(prisma, { log: jest.fn() } as any);
    await expect(service.createBooking({ organizationId: 'org-1', branchId: 'br-1', trainerId: 'tr-1', memberId: 'mem-1', startsAt: '2026-06-18T10:00:00.000Z', endsAt: '2026-06-18T11:00:00.000Z' })).rejects.toBeInstanceOf(BadRequestException);
  });
});
