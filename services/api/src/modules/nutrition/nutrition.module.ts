import { Module } from '@nestjs/common';
import { NutritionController } from './nutrition.controller';
import { NutritionRepository } from './nutrition.repository';
import { NutritionService } from './nutrition.service';

@Module({
  controllers: [NutritionController],
  providers: [NutritionService, NutritionRepository],
  exports: [NutritionService],
})
export class NutritionModule {}
