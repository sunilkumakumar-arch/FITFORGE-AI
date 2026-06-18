import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateProductDto, UpdateProductDto } from './dto/products.dto';
import { ProductsRepository } from './products.repository';

@Injectable()
export class ProductsService extends BaseCrudService<CreateProductDto, UpdateProductDto> {
  constructor(protected readonly repository: ProductsRepository) {
    super(repository);
  }
}
