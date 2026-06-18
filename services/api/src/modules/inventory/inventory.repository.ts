import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateInventoryDto, UpdateInventoryDto } from './dto/inventory.dto';

@Injectable()
export class InventoryRepository extends BaseRepository<CreateInventoryDto, UpdateInventoryDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'inventoryItem');
  }
}
