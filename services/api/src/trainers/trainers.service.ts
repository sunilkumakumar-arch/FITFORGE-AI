import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { AuditService } from '../core/audit.service';
import { PrismaService } from '../core/prisma.service';
import { BookingStatusDto, CreateTrainerAvailabilityDto, CreateTrainerBookingDto } from './dto/trainers.dto';

@Injectable()
export class TrainersService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}
  createAvailability(dto: CreateTrainerAvailabilityDto) { return (this.prisma as any).trainerAvailability.create({ data: { ...dto, startsAt: new Date(dto.startsAt), endsAt: new Date(dto.endsAt) } }); }
  listAvailability(query: any) { return (this.prisma as any).trainerAvailability.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), ...(query.trainerId ? { trainerId: query.trainerId } : {}), isAvailable: true }, orderBy: { startsAt: 'asc' } }); }
  async createBooking(dto: CreateTrainerBookingDto, actorUserId?: string) {
    const startsAt = new Date(dto.startsAt); const endsAt = new Date(dto.endsAt);
    const availability = await (this.prisma as any).trainerAvailability.findFirst({ where: { trainerId: dto.trainerId, branchId: dto.branchId, startsAt: { lte: startsAt }, endsAt: { gte: endsAt }, isAvailable: true } });
    if (!availability) throw new BadRequestException('Trainer is not available for this slot');
    const conflict = await (this.prisma as any).trainerBooking.findFirst({ where: { trainerId: dto.trainerId, status: { in: ['requested', 'confirmed'] }, startsAt: { lt: endsAt }, endsAt: { gt: startsAt } } });
    if (conflict) throw new BadRequestException('Trainer already has a booking in this slot');
    const booking = await (this.prisma as any).trainerBooking.create({ data: { ...dto, startsAt, endsAt } });
    await this.audit.log({ action: 'trainers.booking_create', entityType: 'trainerBooking', entityId: booking.id, actorUserId, organizationId: booking.organizationId, branchId: booking.branchId, afterData: booking });
    return booking;
  }
  listBookings(query: any) { return (this.prisma as any).trainerBooking.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), ...(query.trainerId ? { trainerId: query.trainerId } : {}), ...(query.memberId ? { memberId: query.memberId } : {}) }, orderBy: { startsAt: 'desc' } }); }
  async updateBookingStatus(id: string, dto: BookingStatusDto, actorUserId?: string) { const before = await (this.prisma as any).trainerBooking.findUnique({ where: { id } }); if (!before) throw new NotFoundException('Booking not found'); const updated = await (this.prisma as any).trainerBooking.update({ where: { id }, data: { status: dto.status } }); await this.audit.log({ action: `trainers.booking_${dto.status}`, entityType: 'trainerBooking', entityId: id, actorUserId, organizationId: updated.organizationId, branchId: updated.branchId, beforeData: before, afterData: updated }); return updated; }
}
