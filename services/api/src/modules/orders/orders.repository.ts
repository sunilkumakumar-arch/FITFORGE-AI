import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateOrderDto, UpdateOrderDto } from './dto/orders.dto';

@Injectable()
export class OrdersRepository extends BaseRepository<CreateOrderDto, UpdateOrderDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'order');
  }
}
