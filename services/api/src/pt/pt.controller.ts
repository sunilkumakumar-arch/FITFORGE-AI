import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { ConsumePtCreditDto, CreatePtPackageDto, PurchasePtPackageDto } from './dto/pt.dto';
import { PtService } from './pt.service';

@ApiBearerAuth()
@ApiTags('Personal Training Packages')
@Controller('pt')
export class PtController {
  constructor(private readonly pt: PtService) {}
  @RequirePermissions('bookings.manage') @Post('packages') createPackage(@Body() dto: CreatePtPackageDto) { return this.pt.createPackage(dto); }
  @RequirePermissions('bookings.read') @Get('packages') listPackages(@Query() query: any) { return this.pt.listPackages(query); }
  @RequirePermissions('payments.manage') @Post('purchase') purchase(@Body() dto: PurchasePtPackageDto, @CurrentUser() user: any) { return this.pt.purchasePackage(dto, user?.sub); }
  @RequirePermissions('bookings.manage') @Post('consume-credit') consume(@Body() dto: ConsumePtCreditDto, @CurrentUser() user: any) { return this.pt.consumeCredit(dto, user?.sub); }
  @RequirePermissions('bookings.read') @Get('balance') balance(@Query('memberId') memberId: string, @Query('trainerId') trainerId?: string) { return this.pt.balance(memberId, trainerId); }
}
