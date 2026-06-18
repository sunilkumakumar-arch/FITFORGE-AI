import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateAttendanceDto, UpdateAttendanceDto } from './dto/attendance.dto';
import { AttendanceRepository } from './attendance.repository';

@Injectable()
export class AttendanceService extends BaseCrudService<CreateAttendanceDto, UpdateAttendanceDto> {
  constructor(protected readonly repository: AttendanceRepository) {
    super(repository);
  }

  checkIn(dto: CreateAttendanceDto) {
    return this.create({ ...dto, checkInAt: dto.checkInAt ?? new Date().toISOString() });
  }

  async checkOut(id: string) {
    await this.findOne(id);
    return this.repository.update(id, { checkOutAt: new Date().toISOString() } as unknown as UpdateAttendanceDto);
  }
}
