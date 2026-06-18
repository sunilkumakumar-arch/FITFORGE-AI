import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';

export interface ListOptions {
  page?: number;
  limit?: number;
  where?: Record<string, unknown>;
  orderBy?: Record<string, 'asc' | 'desc'>;
}

@Injectable()
export class BaseRepository<TCreate extends object = Record<string, unknown>, TUpdate extends object = Record<string, unknown>> {
  constructor(
    protected readonly prisma: PrismaService,
    private readonly modelName: string,
  ) {}

  protected get delegate(): any {
    return this.prisma.model(this.modelName);
  }

  create(data: TCreate) {
    return this.delegate.create({ data });
  }

  findMany(options: ListOptions = {}) {
    const page = options.page ?? 1;
    const limit = options.limit ?? 25;
    return this.delegate.findMany({
      where: options.where,
      skip: (page - 1) * limit,
      take: limit,
      orderBy: options.orderBy ?? { createdAt: 'desc' },
    });
  }

  count(where?: Record<string, unknown>) {
    return this.delegate.count({ where });
  }

  findById(id: string) {
    return this.delegate.findUnique({ where: { id } });
  }

  update(id: string, data: TUpdate) {
    return this.delegate.update({ where: { id }, data });
  }

  softDelete(id: string) {
    return this.delegate.update({ where: { id }, data: { deletedAt: new Date() } });
  }
}
