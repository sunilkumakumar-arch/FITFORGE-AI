import { Body, Controller, Get, Param, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { CreateMembershipDto, CreateMembershipPlanDto, MembershipStatusDto, RenewMembershipDto, UpdateMembershipPlanDto } from './dto/membership.dto';
import { MembershipsService } from './memberships.service';

@ApiBearerAuth()
@ApiTags('Membership Management')
@Controller()
export class MembershipsController {
  constructor(private readonly memberships: MembershipsService) {}

  @RequirePermissions('memberships.manage')
  @Post('membership-plans')
  createPlan(@Body() dto: CreateMembershipPlanDto) { return this.memberships.createPlan(dto); }

  @RequirePermissions('memberships.read')
  @Get('membership-plans')
  listPlans(@Query() query: any) { return this.memberships.listPlans(query); }

  @RequirePermissions('memberships.manage')
  @Patch('membership-plans/:id')
  updatePlan(@Param('id') id: string, @Body() dto: UpdateMembershipPlanDto) { return this.memberships.updatePlan(id, dto); }

  @RequirePermissions('memberships.manage')
  @Post('memberships')
  createMembership(@Body() dto: CreateMembershipDto, @CurrentUser() user: any) { return this.memberships.createMembership(dto, user?.sub); }

  @RequirePermissions('memberships.read')
  @Get('memberships')
  listMemberships(@Query() query: any) { return this.memberships.listMemberships(query); }

  @RequirePermissions('memberships.renew')
  @Post('memberships/:id/renew')
  renew(@Param('id') id: string, @Body() dto: RenewMembershipDto, @CurrentUser() user: any) { return this.memberships.renewMembership(id, dto, user?.sub); }

  @RequirePermissions('memberships.manage')
  @Patch('memberships/:id/status')
  updateStatus(@Param('id') id: string, @Body() dto: MembershipStatusDto, @CurrentUser() user: any) { return this.memberships.updateStatus(id, dto, user?.sub); }
}
