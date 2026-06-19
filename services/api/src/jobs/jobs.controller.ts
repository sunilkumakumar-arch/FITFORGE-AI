import { Body, Controller, Post } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { RequirePermissions } from '../auth/permissions.decorator';
import { JobsService } from './jobs.service';

@ApiBearerAuth()
@ApiTags('Production Jobs')
@Controller('jobs')
export class JobsController {
  constructor(private readonly jobs: JobsService) {}
  @RequirePermissions('system.jobs') @Post('release-expired-reservations') releaseExpiredReservations() { return this.jobs.releaseExpiredReservations(); }
  @RequirePermissions('system.jobs') @Post('scan-membership-renewals') scanMembershipRenewals(@Body('daysAhead') daysAhead?: number) { return this.jobs.scanMembershipRenewals(daysAhead); }
  @RequirePermissions('system.jobs') @Post('reconcile-razorpay') reconcileRazorpay() { return this.jobs.reconcileRazorpayPayments(); }
  @RequirePermissions('system.jobs') @Post('aggregate-daily-branch-metrics') aggregate(@Body('date') date?: string) { return this.jobs.aggregateDailyBranchMetrics(date ? new Date(date) : new Date()); }
}
