import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateExerciseDto, UpdateExerciseDto } from './dto/exercises.dto';

@Injectable()
export class ExercisesRepository extends BaseRepository<CreateExerciseDto, UpdateExerciseDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'exercise');
  }
}
