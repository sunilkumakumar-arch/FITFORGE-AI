import { Injectable } from '@nestjs/common';
import { AuditService } from '../core/audit.service';
import { PrismaService } from '../core/prisma.service';
import { CreateExerciseDto, CreateWorkoutProgramDto } from './dto/workouts.dto';

@Injectable()
export class WorkoutsService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}
  createExercise(dto: CreateExerciseDto) { return (this.prisma as any).exercise.create({ data: dto }); }
  listExercises(query: any) { return (this.prisma as any).exercise.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}) }, orderBy: { name: 'asc' } }); }
  async createProgram(dto: CreateWorkoutProgramDto, actorUserId?: string) { const program = await (this.prisma as any).workoutProgram.create({ data: { ...dto, exercises: dto.exercises ?? [] } }); await this.audit.log({ action: 'workouts.program_create', entityType: 'workoutProgram', entityId: program.id, actorUserId, organizationId: program.organizationId, branchId: program.branchId, afterData: program }); return program; }
  listPrograms(query: any) { return (this.prisma as any).workoutProgram.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), ...(query.memberId ? { memberId: query.memberId } : {}), ...(query.trainerId ? { trainerId: query.trainerId } : {}) }, orderBy: { createdAt: 'desc' } }); }
}
