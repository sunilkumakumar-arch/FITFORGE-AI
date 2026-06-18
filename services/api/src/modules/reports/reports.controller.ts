import { Controller, Get, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { ReportsService } from './reports.service';

@ApiBearerAuth()
@ApiTags('Reporting & Analytics')
@Controller('reports')
export class ReportsController {
  constructor(private readonly reportsService: ReportsService) {}

  @RequirePermissions(Permission.ReportsRead)
  @Get('dashboard')
  dashboard(@Query('organizationId') organizationId?: string, @Query('branchId') branchId?: string) {
    return this.reportsService.dashboard(organizationId, branchId);
  }
}
