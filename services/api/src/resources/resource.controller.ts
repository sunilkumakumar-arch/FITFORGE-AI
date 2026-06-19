import { Body, Controller, Delete, Get, Param, Patch, Post, Query, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { AuthGuard } from '../auth/auth.guard';
import { CurrentUser } from '../auth/current-user.decorator';
import { RbacGuard } from '../auth/rbac.guard';
import { ResourceService } from './resource.service';

@ApiBearerAuth()
@ApiTags('Production Resources')
@Controller()
@UseGuards(AuthGuard, RbacGuard)
export class ResourceController {
  constructor(private readonly service: ResourceService) {}
  @Post(':resource') create(@Param('resource') resource: string, @Body() dto: any, @CurrentUser() user: any) { return this.service.create(resource, dto, user?.sub); }
  @Get(':resource') list(@Param('resource') resource: string, @Query() query: any) { return this.service.list(resource, query); }
  @Get(':resource/:id') get(@Param('resource') resource: string, @Param('id') id: string) { return this.service.get(resource, id); }
  @Patch(':resource/:id') update(@Param('resource') resource: string, @Param('id') id: string, @Body() dto: any, @CurrentUser() user: any) { return this.service.update(resource, id, dto, user?.sub); }
  @Delete(':resource/:id') remove(@Param('resource') resource: string, @Param('id') id: string, @CurrentUser() user: any) { return this.service.remove(resource, id, user?.sub); }
}
