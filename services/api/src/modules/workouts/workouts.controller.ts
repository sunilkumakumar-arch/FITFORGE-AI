import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateWorkoutDto, UpdateWorkoutDto } from './dto/workouts.dto';
import { WorkoutsService } from './workouts.service';

@ApiBearerAuth()
@ApiTags('Workout Planning')
@Controller('workout-plans')
export class WorkoutsController {
  constructor(private readonly service: WorkoutsService) {}

  @RequirePermissions(Permission.WorkoutsManage)
  @Post()
  create(@Body() dto: CreateWorkoutDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.WorkoutsRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.WorkoutsRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.WorkoutsManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateWorkoutDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.WorkoutsManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
