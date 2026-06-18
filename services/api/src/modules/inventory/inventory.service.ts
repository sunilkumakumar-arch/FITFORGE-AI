import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateInventoryDto, UpdateInventoryDto } from './dto/inventory.dto';
import { InventoryRepository } from './inventory.repository';

@Injectable()
export class InventoryService extends BaseCrudService<CreateInventoryDto, UpdateInventoryDto> {
  constructor(protected readonly repository: InventoryRepository) {
    super(repository);
  }
}
