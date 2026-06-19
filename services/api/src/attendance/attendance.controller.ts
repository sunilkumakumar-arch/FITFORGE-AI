import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { CreateQrTokenDto, ManualCheckInDto, QrCheckInDto } from './dto/attendance.dto';
import { AttendanceService } from './attendance.service';

@ApiBearerAuth()
@ApiTags('QR Attendance')
@Controller('attendance')
export class AttendanceController {
  constructor(private readonly attendance: AttendanceService) {}

  @RequirePermissions('attendance.manage')
  @Post('qr-token')
  createQrToken(@Body() dto: CreateQrTokenDto) { return this.attendance.createQrToken(dto); }

  @RequirePermissions('attendance.check_in')
  @Post('qr-check-in')
  qrCheckIn(@Body() dto: QrCheckInDto, @CurrentUser() user: any) { return this.attendance.qrCheckIn(dto, user?.sub); }

  @RequirePermissions('attendance.manage')
  @Post('manual-check-in')
  manualCheckIn(@Body() dto: ManualCheckInDto, @CurrentUser() user: any) { return this.attendance.manualCheckIn(dto, user?.sub); }

  @RequirePermissions('attendance.read')
  @Get()
  list(@Query() query: any) { return this.attendance.list(query); }

  @RequirePermissions('attendance.manage')
  @Post(':id/check-out') checkOut(@Param('id') id: string) { return this.attendance.checkOut(id); }
}
