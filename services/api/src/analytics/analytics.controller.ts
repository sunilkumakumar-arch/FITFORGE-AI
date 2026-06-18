import { Controller, Get, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { PrismaService } from '../core/prisma.service';

@ApiBearerAuth()
@ApiTags('Revenue Analytics')
@Controller('analytics')
export class AnalyticsController {
  constructor(private readonly prisma: PrismaService) {}
  @Get('revenue') async revenue(@Query('organizationId') organizationId?: string, @Query('branchId') branchId?: string) {
    const where: any = { status: 'paid' }; if (organizationId) where.organizationId = organizationId; if (branchId) where.branchId = branchId;
    const payments = await (this.prisma as any).payment.findMany({ where });
    const revenueMinor = payments.reduce((sum: number, p: any) => sum + p.amountMinor, 0);
    return { revenueMinor, payments: payments.length, currency: payments[0]?.currency ?? 'INR' };
  }
  @Get('dashboard') async dashboard(@Query('organizationId') organizationId?: string, @Query('branchId') branchId?: string) {
    const scoped: any = {}; if (organizationId) scoped.organizationId = organizationId; if (branchId) scoped.branchId = branchId;
    const [memberships, attendance, orders, payments] = await Promise.all([
      (this.prisma as any).membership.count({ where: scoped }),
      (this.prisma as any).attendanceLog.count({ where: scoped }),
      (this.prisma as any).order.count({ where: scoped }),
      (this.prisma as any).payment.count({ where: { ...scoped, status: 'paid' } }),
    ]);
    return { memberships, attendance, orders, paidPayments: payments };
  }
}
