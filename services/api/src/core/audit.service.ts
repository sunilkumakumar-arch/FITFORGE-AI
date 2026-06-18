import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Injectable()
export class AuditService {
  constructor(private readonly prisma: PrismaService) {}
  async log(input: { action: string; entityType: string; entityId?: string; actorUserId?: string; organizationId?: string; branchId?: string; beforeData?: unknown; afterData?: unknown }) {
    await (this.prisma as any).auditLog.create({ data: input }).catch(() => undefined);
  }
}
