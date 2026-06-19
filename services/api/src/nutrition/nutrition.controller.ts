import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { CreateNutritionPlanDto, MacroCalculatorDto } from './dto/nutrition.dto';
import { NutritionService } from './nutrition.service';

@ApiBearerAuth()
@ApiTags('Nutrition Management')
@Controller('nutrition-plans')
export class NutritionController {
  constructor(private readonly nutrition: NutritionService) {}
  @RequirePermissions('nutrition.manage') @Post() createPlan(@Body() dto: CreateNutritionPlanDto, @CurrentUser() user: any) { return this.nutrition.createPlan(dto, user?.sub); }
  @RequirePermissions('nutrition.read') @Get() listPlans(@Query() query: any) { return this.nutrition.listPlans(query); }
  @RequirePermissions('nutrition.read') @Post('calculate-macros') calculateMacros(@Body() dto: MacroCalculatorDto) { return this.nutrition.calculateMacros(dto); }
}
