import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateProgresDto, UpdateProgresDto } from './dto/progress.dto';
import { ProgressService } from './progress.service';

@ApiBearerAuth()
@ApiTags('Progress Tracking')
@Controller('progress')
export class ProgressController {
  constructor(private readonly service: ProgressService) {}

  @RequirePermissions(Permission.ProgressManage)
  @Post()
  create(@Body() dto: CreateProgresDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.ProgressRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.ProgressRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.ProgressManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateProgresDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.ProgressManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
