import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../core/prisma.service';
import { AuditService } from '../core/audit.service';
import { resourceMap } from './resource-map';

@Injectable()
export class ResourceService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}
  meta(resource: string) { const meta = resourceMap[resource]; if (!meta) throw new BadRequestException(`Unsupported resource: ${resource}`); return meta; }
  async create(resource: string, data: any, actorUserId?: string) {
    const meta = this.meta(resource);
    const item = await this.prisma.delegate(meta.model).create({ data });
    await this.audit.log({ action: `${resource}.create`, entityType: resource, entityId: item.id, actorUserId, organizationId: data.organizationId, branchId: data.branchId, afterData: item });
    return item;
  }
  list(resource: string, query: any) {
    const meta = this.meta(resource);
    const page = Number(query.page ?? 1); const limit = Math.min(Number(query.limit ?? 25), 100);
    const where: any = {};
    if (query.organizationId) where.organizationId = query.organizationId;
    if (query.branchId) where.branchId = query.branchId;
    return this.prisma.delegate(meta.model).findMany({ where, skip: (page - 1) * limit, take: limit, orderBy: { createdAt: 'desc' } }).catch(() => this.prisma.delegate(meta.model).findMany({ where, skip: (page - 1) * limit, take: limit }));
  }
  async get(resource: string, id: string) { const item = await this.prisma.delegate(this.meta(resource).model).findUnique({ where: { id } }); if (!item) throw new NotFoundException('Resource not found'); return item; }
  async update(resource: string, id: string, data: any, actorUserId?: string) { const beforeData = await this.get(resource, id); const item = await this.prisma.delegate(this.meta(resource).model).update({ where: { id }, data }); await this.audit.log({ action: `${resource}.update`, entityType: resource, entityId: id, actorUserId, beforeData, afterData: item }); return item; }
  async remove(resource: string, id: string, actorUserId?: string) { const beforeData = await this.get(resource, id); await this.prisma.delegate(this.meta(resource).model).delete({ where: { id } }); await this.audit.log({ action: `${resource}.delete`, entityType: resource, entityId: id, actorUserId, beforeData }); return { deleted: true }; }
}
