import { Body, Controller, Param, Post } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { AttendanceService } from './attendance.service';

@ApiBearerAuth()
@ApiTags('QR Attendance')
@Controller('attendance')
export class AttendanceController {
  constructor(private readonly attendance: AttendanceService) {}
  @Post('qr-token') createQrToken(@Body('branchId') branchId: string, @Body('ttlSeconds') ttlSeconds?: number) { return this.attendance.createQrToken(branchId, ttlSeconds); }
  @Post('qr-check-in') qrCheckIn(@Body() dto: any, @CurrentUser() user: any) { return this.attendance.qrCheckIn(dto, user?.sub); }
  @Post(':id/check-out') checkOut(@Param('id') id: string) { return this.attendance.checkOut(id); }
}
