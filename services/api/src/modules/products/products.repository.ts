import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateProductDto, UpdateProductDto } from './dto/products.dto';

@Injectable()
export class ProductsRepository extends BaseRepository<CreateProductDto, UpdateProductDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'product');
  }
}
