import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../shared/database/prisma.service';

@Injectable()
export class ReportsService {
  constructor(private readonly prisma: PrismaService) {}

  async dashboard(organizationId?: string, branchId?: string) {
    const scoped = { organizationId, ...(branchId ? { branchId } : {}) };
    const [memberships, attendance, orders, postureSessions] = await Promise.all([
      (this.prisma as any).membership.count({ where: scoped }),
      (this.prisma as any).attendanceLog.count({ where: scoped }),
      (this.prisma as any).order.count({ where: scoped }),
      (this.prisma as any).postureSession.count({ where: scoped }),
    ]);
    return { memberships, attendance, orders, postureSessions };
  }
}
