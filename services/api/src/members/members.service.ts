import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../core/prisma.service';

@Injectable()
export class MembersService {
  constructor(private readonly prisma: PrismaService) {}

  async getSummary(memberId: string) {
    const member = await (this.prisma as any).user.findUnique({
      where: { id: memberId },
      select: { id: true, email: true, phone: true, firstName: true, lastName: true, status: true },
    });
    if (!member) throw new NotFoundException('Member not found');

    const membership = await this.findCurrentMembership(memberId);
    const trainer = await this.findAssignedTrainer(memberId);
    const ptPackage = await this.findPtPackageSummary(memberId);

    return {
      member,
      membership: membership
        ? {
            planName: membership.plan?.name ?? null,
            status: membership.status,
            expiry: membership.endDate?.toISOString?.() ?? membership.endDate,
            remainingDays: this.remainingDays(membership.endDate),
          }
        : { planName: null, status: null, expiry: null, remainingDays: null },
      trainer: trainer
        ? { id: trainer.id, firstName: trainer.firstName, lastName: trainer.lastName }
        : { id: null, firstName: null, lastName: null },
      ptPackage,
    };
  }

  private async findCurrentMembership(memberId: string) {
    const active = await (this.prisma as any).membership.findFirst({
      where: { memberId, status: 'active', endDate: { gte: new Date() } },
      include: { plan: true },
      orderBy: { endDate: 'desc' },
    });
    if (active) return active;

    return (this.prisma as any).membership.findFirst({
      where: { memberId },
      include: { plan: true },
      orderBy: { endDate: 'desc' },
    });
  }

  private async findAssignedTrainer(memberId: string) {
    const ptAssignment = await (this.prisma as any).ptCreditLedger.findFirst({
      where: { memberId, trainerId: { not: null }, creditsDelta: { gt: 0 } },
      orderBy: { createdAt: 'desc' },
    });
    if (ptAssignment?.trainerId) {
      return (this.prisma as any).user.findUnique({
        where: { id: ptAssignment.trainerId },
        select: { id: true, firstName: true, lastName: true },
      });
    }

    const program = await (this.prisma as any).workoutProgram.findFirst({
      where: { memberId, trainerId: { not: null } },
      orderBy: { createdAt: 'desc' },
    });
    if (program?.trainerId) {
      return (this.prisma as any).user.findUnique({
        where: { id: program.trainerId },
        select: { id: true, firstName: true, lastName: true },
      });
    }

    const booking = await (this.prisma as any).trainerBooking.findFirst({
      where: { memberId, status: { in: ['requested', 'confirmed', 'completed'] } },
      orderBy: { createdAt: 'desc' },
    });
    if (booking?.trainerId) {
      return (this.prisma as any).user.findUnique({
        where: { id: booking.trainerId },
        select: { id: true, firstName: true, lastName: true },
      });
    }

    return null;
  }

  private async findPtPackageSummary(memberId: string) {
    const purchase = await (this.prisma as any).ptCreditLedger.findFirst({
      where: {
        memberId,
        packageId: { not: null },
        creditsDelta: { gt: 0 },
        OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }],
      },
      orderBy: { createdAt: 'desc' },
    });

    if (!purchase) {
      return { name: null, expiry: null, remainingSessions: 0 };
    }

    const pkg = purchase.packageId
      ? await (this.prisma as any).ptPackage.findUnique({ where: { id: purchase.packageId } })
      : null;

    const entries = await (this.prisma as any).ptCreditLedger.findMany({
      where: {
        memberId,
        OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }],
      },
    });
    const remainingSessions = entries.reduce((sum: number, entry: any) => sum + entry.creditsDelta, 0);

    return {
      name: pkg?.name ?? null,
      expiry: purchase.expiresAt?.toISOString?.() ?? purchase.expiresAt ?? null,
      remainingSessions: Math.max(remainingSessions, 0),
    };
  }

  private remainingDays(endDate?: Date | string | null) {
    if (!endDate) return null;
    const expiry = endDate instanceof Date ? endDate : new Date(endDate);
    const diffMs = expiry.getTime() - Date.now();
    if (diffMs <= 0) return 0;
    return Math.ceil(diffMs / (24 * 60 * 60 * 1000));
  }
}
