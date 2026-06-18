import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateWorkoutDto, UpdateWorkoutDto } from './dto/workouts.dto';
import { WorkoutsRepository } from './workouts.repository';

@Injectable()
export class WorkoutsService extends BaseCrudService<CreateWorkoutDto, UpdateWorkoutDto> {
  constructor(protected readonly repository: WorkoutsRepository) {
    super(repository);
  }
}
