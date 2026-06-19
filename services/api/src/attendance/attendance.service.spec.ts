import { BadRequestException } from '@nestjs/common';
import { AttendanceService } from './attendance.service';

describe('AttendanceService', () => {
  it('prevents duplicate manual check-ins in the duplicate window', async () => {
    const prisma: any = {
      attendanceLog: {
        findFirst: jest.fn().mockResolvedValue({ id: 'existing' }),
        create: jest.fn(),
      },
    };
    const service = new AttendanceService(prisma, { log: jest.fn() } as any);
    await expect(service.manualCheckIn({ organizationId: 'org-1', branchId: 'br-1', memberId: 'mem-1' })).rejects.toBeInstanceOf(BadRequestException);
    expect(prisma.attendanceLog.create).not.toHaveBeenCalled();
  });
});
