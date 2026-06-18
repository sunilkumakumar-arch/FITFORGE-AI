import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateNutritionDto, UpdateNutritionDto } from './dto/nutrition.dto';
import { NutritionRepository } from './nutrition.repository';

@Injectable()
export class NutritionService extends BaseCrudService<CreateNutritionDto, UpdateNutritionDto> {
  constructor(protected readonly repository: NutritionRepository) {
    super(repository);
  }
}
