import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateOrderDto, UpdateOrderDto } from './dto/orders.dto';
import { OrdersRepository } from './orders.repository';

@Injectable()
export class OrdersService extends BaseCrudService<CreateOrderDto, UpdateOrderDto> {
  constructor(protected readonly repository: OrdersRepository) {
    super(repository);
  }
}
