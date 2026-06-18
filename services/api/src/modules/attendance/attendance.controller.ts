import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateAttendanceDto, UpdateAttendanceDto } from './dto/attendance.dto';
import { AttendanceService } from './attendance.service';

@ApiBearerAuth()
@ApiTags('Attendance')
@Controller('attendance')
export class AttendanceController {
  constructor(private readonly service: AttendanceService) {}

  @RequirePermissions(Permission.AttendanceManage)
  @Post()
  create(@Body() dto: CreateAttendanceDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.AttendanceManage)
  @Post('check-in')
  checkIn(@Body() dto: CreateAttendanceDto) {
    return this.service.checkIn(dto);
  }

  @RequirePermissions(Permission.AttendanceManage)
  @Post(':id/check-out')
  checkOut(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.checkOut(id);
  }

  @RequirePermissions(Permission.AttendanceRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.AttendanceRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.AttendanceManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateAttendanceDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.AttendanceManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
