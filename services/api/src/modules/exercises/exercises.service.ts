import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateExerciseDto, UpdateExerciseDto } from './dto/exercises.dto';
import { ExercisesRepository } from './exercises.repository';

@Injectable()
export class ExercisesService extends BaseCrudService<CreateExerciseDto, UpdateExerciseDto> {
  constructor(protected readonly repository: ExercisesRepository) {
    super(repository);
  }
}
