import { Injectable } from '@nestjs/common';
import { AuditService } from '../core/audit.service';
import { PrismaService } from '../core/prisma.service';
import { CreateNutritionPlanDto, MacroCalculatorDto } from './dto/nutrition.dto';

@Injectable()
export class NutritionService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}
  calculateMacros(dto: MacroCalculatorDto) { const bmr = dto.sex === 'male' ? 10 * dto.weightKg + 6.25 * dto.heightCm - 5 * dto.age + 5 : 10 * dto.weightKg + 6.25 * dto.heightCm - 5 * dto.age - 161; const multiplier = dto.goal === 'fat_loss' ? 0.85 : dto.goal === 'muscle_gain' ? 1.12 : 1; const calories = Math.round(bmr * 1.45 * multiplier); const proteinGrams = Math.round(dto.weightKg * 2); const fatGrams = Math.round((calories * 0.25) / 9); const carbsGrams = Math.round((calories - proteinGrams * 4 - fatGrams * 9) / 4); return { calories, proteinGrams, carbsGrams, fatGrams }; }
  async createPlan(dto: CreateNutritionPlanDto, actorUserId?: string) { const plan = await (this.prisma as any).nutritionPlan.create({ data: { ...dto, meals: dto.meals ?? [] } }); await this.audit.log({ action: 'nutrition.plan_create', entityType: 'nutritionPlan', entityId: plan.id, actorUserId, organizationId: plan.organizationId, branchId: plan.branchId, afterData: plan }); return plan; }
  listPlans(query: any) { return (this.prisma as any).nutritionPlan.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}), ...(query.memberId ? { memberId: query.memberId } : {}), ...(query.coachId ? { coachId: query.coachId } : {}) }, orderBy: { createdAt: 'desc' } }); }
}
