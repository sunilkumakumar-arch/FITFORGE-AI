import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreatePostureDto, UpdatePostureDto } from './dto/posture.dto';
import { PostureService } from './posture.service';

@ApiBearerAuth()
@ApiTags('AI Posture Analysis')
@Controller('posture')
export class PostureController {
  constructor(private readonly service: PostureService) {}

  @RequirePermissions(Permission.PostureManage)
  @Post()
  create(@Body() dto: CreatePostureDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.PostureManage)
  @Post('analyze-frame')
  analyzeFrame(@Body() dto: Record<string, unknown>) {
    return this.service.analyzeFrame(dto as any);
  }

  @RequirePermissions(Permission.PostureRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.PostureRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.PostureManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdatePostureDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.PostureManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
