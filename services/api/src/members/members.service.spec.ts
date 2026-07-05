import { NotFoundException } from '@nestjs/common';
import { MembersService } from './members.service';

describe('MembersService', () => {
  const memberId = 'member-1';
  const trainerId = 'trainer-1';
  const now = new Date('2026-07-05T00:00:00.000Z');

  beforeAll(() => {
    jest.useFakeTimers();
    jest.setSystemTime(now);
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  it('returns a member summary with membership, trainer, and PT package details', async () => {
    const prisma: any = {
      user: {
        findUnique: jest
          .fn()
          .mockResolvedValueOnce({ id: memberId, email: 'member@test.com', phone: '+911', firstName: 'Alex', lastName: 'Member', status: 'active' })
          .mockResolvedValueOnce({ id: trainerId, firstName: 'Taylor', lastName: 'Trainer' }),
      },
      membership: {
        findFirst: jest.fn().mockResolvedValue({
          status: 'active',
          endDate: new Date('2026-08-01T00:00:00.000Z'),
          plan: { name: 'Monthly Plan' },
        }),
      },
      ptCreditLedger: {
        findFirst: jest.fn().mockResolvedValue({
          trainerId,
          packageId: 'pkg-1',
          creditsDelta: 10,
          expiresAt: new Date('2026-09-01T00:00:00.000Z'),
        }),
        findMany: jest.fn().mockResolvedValue([{ creditsDelta: 10 }, { creditsDelta: -2 }]),
      },
      ptPackage: {
        findUnique: jest.fn().mockResolvedValue({ name: '10 Session Pack' }),
      },
      workoutProgram: { findFirst: jest.fn().mockResolvedValue(null) },
      trainerBooking: { findFirst: jest.fn().mockResolvedValue(null) },
    };

    const service = new MembersService(prisma);
    const summary = await service.getSummary(memberId);

    expect(summary.member.firstName).toBe('Alex');
    expect(summary.membership.planName).toBe('Monthly Plan');
    expect(summary.membership.remainingDays).toBe(27);
    expect(summary.trainer.firstName).toBe('Taylor');
    expect(summary.ptPackage.name).toBe('10 Session Pack');
    expect(summary.ptPackage.remainingSessions).toBe(8);
  });

  it('throws when the member does not exist', async () => {
    const prisma: any = { user: { findUnique: jest.fn().mockResolvedValue(null) } };
    const service = new MembersService(prisma);
    await expect(service.getSummary('missing')).rejects.toBeInstanceOf(NotFoundException);
  });
});
