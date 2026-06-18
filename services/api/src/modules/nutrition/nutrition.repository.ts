import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateNutritionDto, UpdateNutritionDto } from './dto/nutrition.dto';

@Injectable()
export class NutritionRepository extends BaseRepository<CreateNutritionDto, UpdateNutritionDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'nutritionPlan');
  }
}
