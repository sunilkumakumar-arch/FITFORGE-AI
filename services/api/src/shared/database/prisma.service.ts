import { Injectable, Logger, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(PrismaService.name);

  async onModuleInit() {
    await this.$connect();
    this.logger.log('Connected to PostgreSQL');
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }

  model<T = any>(name: string): T {
    const delegate = (this as unknown as Record<string, T>)[name];
    if (!delegate) {
      throw new Error(`Prisma model delegate not found: ${name}`);
    }
    return delegate;
  }
}
