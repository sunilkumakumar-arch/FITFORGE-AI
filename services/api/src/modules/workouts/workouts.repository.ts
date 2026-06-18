import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateWorkoutDto, UpdateWorkoutDto } from './dto/workouts.dto';

@Injectable()
export class WorkoutsRepository extends BaseRepository<CreateWorkoutDto, UpdateWorkoutDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'workoutPlan');
  }
}
