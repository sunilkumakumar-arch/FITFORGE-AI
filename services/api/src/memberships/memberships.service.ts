import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { AuditService } from '../core/audit.service';
import { PrismaService } from '../core/prisma.service';
import { CreateMembershipDto, CreateMembershipPlanDto, MembershipStatusDto, RenewMembershipDto, UpdateMembershipPlanDto } from './dto/membership.dto';

@Injectable()
export class MembershipsService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}

  createPlan(dto: CreateMembershipPlanDto) {
    return (this.prisma as any).membershipPlan.create({ data: { ...dto, currency: dto.currency ?? 'INR' } });
  }

  listPlans(query: any) {
    return (this.prisma as any).membershipPlan.findMany({ where: this.scope(query), orderBy: { name: 'asc' } });
  }

  updatePlan(id: string, dto: UpdateMembershipPlanDto) {
    return (this.prisma as any).membershipPlan.update({ where: { id }, data: dto });
  }

  async createMembership(dto: CreateMembershipDto, actorUserId?: string) {
    const plan = await this.getActivePlan(dto.planId);
    if (plan.organizationId !== dto.organizationId) throw new BadRequestException('Plan does not belong to organization');
    if (plan.branchId && plan.branchId !== dto.branchId) throw new BadRequestException('Plan is not available for this branch');
    const startDate = dto.startDate ? new Date(dto.startDate) : new Date();
    const endDate = dto.endDate ? new Date(dto.endDate) : this.addDays(startDate, plan.durationDays);
    const membership = await (this.prisma as any).membership.create({
      data: { organizationId: dto.organizationId, branchId: dto.branchId, memberId: dto.memberId, planId: dto.planId, startDate, endDate, autoRenew: dto.autoRenew ?? false, status: dto.activateImmediately === false ? 'pending' : 'active' },
    });
    await this.audit.log({ action: 'memberships.create', entityType: 'membership', entityId: membership.id, actorUserId, organizationId: dto.organizationId, branchId: dto.branchId, afterData: membership });
    return membership;
  }

  listMemberships(query: any) {
    return (this.prisma as any).membership.findMany({ where: this.scope(query), include: { plan: true, member: true, branch: true }, orderBy: { createdAt: 'desc' } });
  }

  async renewMembership(id: string, dto: RenewMembershipDto, actorUserId?: string) {
    const membership = await (this.prisma as any).membership.findUnique({ where: { id }, include: { plan: true } });
    if (!membership) throw new NotFoundException('Membership not found');
    const plan = dto.planId ? await this.getActivePlan(dto.planId) : membership.plan;
    const baseDate = membership.endDate > new Date() ? membership.endDate : new Date();
    const renewed = await (this.prisma as any).membership.update({
      where: { id },
      data: { planId: plan.id, startDate: membership.startDate, endDate: this.addDays(baseDate, plan.durationDays), status: dto.activateImmediately === false ? 'pending' : 'active' },
    });
    await this.audit.log({ action: 'memberships.renew', entityType: 'membership', entityId: id, actorUserId, organizationId: renewed.organizationId, branchId: renewed.branchId, beforeData: membership, afterData: { renewed, paymentId: dto.paymentId } });
    return renewed;
  }

  async updateStatus(id: string, dto: MembershipStatusDto, actorUserId?: string) {
    const before = await (this.prisma as any).membership.findUnique({ where: { id } });
    if (!before) throw new NotFoundException('Membership not found');
    const updated = await (this.prisma as any).membership.update({ where: { id }, data: { status: dto.status } });
    await this.audit.log({ action: `memberships.${dto.status}`, entityType: 'membership', entityId: id, actorUserId, organizationId: updated.organizationId, branchId: updated.branchId, beforeData: before, afterData: updated });
    return updated;
  }

  private async getActivePlan(id: string) {
    const plan = await (this.prisma as any).membershipPlan.findUnique({ where: { id } });
    if (!plan || !plan.isActive) throw new NotFoundException('Active membership plan not found');
    return plan;
  }

  private addDays(date: Date, days: number) {
    return new Date(date.getTime() + days * 24 * 60 * 60 * 1000);
  }

  private scope(query: any) {
    return { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}) };
  }
}
