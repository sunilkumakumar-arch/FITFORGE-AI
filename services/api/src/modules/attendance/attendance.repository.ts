import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateAttendanceDto, UpdateAttendanceDto } from './dto/attendance.dto';

@Injectable()
export class AttendanceRepository extends BaseRepository<CreateAttendanceDto, UpdateAttendanceDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'attendanceLog');
  }
}
