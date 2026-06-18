import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateProgresDto, UpdateProgresDto } from './dto/progress.dto';
import { ProgressRepository } from './progress.repository';

@Injectable()
export class ProgressService extends BaseCrudService<CreateProgresDto, UpdateProgresDto> {
  constructor(protected readonly repository: ProgressRepository) {
    super(repository);
  }
}
