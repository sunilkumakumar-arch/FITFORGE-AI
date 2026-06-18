import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateMembershipDto, UpdateMembershipDto } from './dto/memberships.dto';
import { MembershipsService } from './memberships.service';

@ApiBearerAuth()
@ApiTags('Memberships')
@Controller('memberships')
export class MembershipsController {
  constructor(private readonly service: MembershipsService) {}

  @RequirePermissions(Permission.MembershipsManage)
  @Post()
  create(@Body() dto: CreateMembershipDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.MembershipsRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.MembershipsRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.MembershipsManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateMembershipDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.MembershipsManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
