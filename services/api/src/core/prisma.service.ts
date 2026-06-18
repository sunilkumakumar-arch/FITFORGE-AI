import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() { await this.$connect(); }
  async onModuleDestroy() { await this.$disconnect(); }
  delegate(model: string): any {
    const value = (this as unknown as Record<string, unknown>)[model];
    if (!value) throw new Error(`Unknown Prisma model: ${model}`);
    return value;
  }
}
