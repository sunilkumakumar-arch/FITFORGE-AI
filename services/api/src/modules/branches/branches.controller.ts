import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateBranchDto, UpdateBranchDto } from './dto/branches.dto';
import { BranchesService } from './branches.service';

@ApiBearerAuth()
@ApiTags('Branches')
@Controller('branches')
export class BranchesController {
  constructor(private readonly service: BranchesService) {}

  @RequirePermissions(Permission.BranchesManage)
  @Post()
  create(@Body() dto: CreateBranchDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.BranchesRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.BranchesRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.BranchesManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateBranchDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.BranchesManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
