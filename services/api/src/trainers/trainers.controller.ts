import { Body, Controller, Get, Param, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { BookingStatusDto, CreateTrainerAvailabilityDto, CreateTrainerBookingDto } from './dto/trainers.dto';
import { TrainersService } from './trainers.service';

@ApiBearerAuth()
@ApiTags('Trainer Management')
@Controller('trainers')
export class TrainersController {
  constructor(private readonly trainers: TrainersService) {}
  @RequirePermissions('bookings.manage') @Post('availability') createAvailability(@Body() dto: CreateTrainerAvailabilityDto) { return this.trainers.createAvailability(dto); }
  @RequirePermissions('bookings.read') @Get('availability') listAvailability(@Query() query: any) { return this.trainers.listAvailability(query); }
  @RequirePermissions('bookings.manage') @Post('bookings') createBooking(@Body() dto: CreateTrainerBookingDto, @CurrentUser() user: any) { return this.trainers.createBooking(dto, user?.sub); }
  @RequirePermissions('bookings.read') @Get('bookings') listBookings(@Query() query: any) { return this.trainers.listBookings(query); }
  @RequirePermissions('bookings.manage') @Patch('bookings/:id/status') updateStatus(@Param('id') id: string, @Body() dto: BookingStatusDto, @CurrentUser() user: any) { return this.trainers.updateBookingStatus(id, dto, user?.sub); }
}
