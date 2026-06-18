import { NotFoundException } from '@nestjs/common';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { BaseRepository } from './base.repository';

export class BaseCrudService<TCreate extends object, TUpdate extends object> {
  constructor(protected readonly repository: BaseRepository<TCreate, TUpdate>) {}

  async create(dto: TCreate) {
    return this.repository.create(dto);
  }

  async findAll(query: PaginationQueryDto) {
    const [items, total] = await Promise.all([
      this.repository.findMany({ page: query.page, limit: query.limit }),
      this.repository.count(),
    ]);
    return { items, total, page: query.page, limit: query.limit };
  }

  async findOne(id: string) {
    const entity = await this.repository.findById(id);
    if (!entity) {
      throw new NotFoundException('Resource not found');
    }
    return entity;
  }

  async update(id: string, dto: TUpdate) {
    await this.findOne(id);
    return this.repository.update(id, dto);
  }

  async remove(id: string) {
    await this.findOne(id);
    return this.repository.softDelete(id);
  }
}
