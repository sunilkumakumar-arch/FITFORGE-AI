import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateExerciseDto, UpdateExerciseDto } from './dto/exercises.dto';
import { ExercisesService } from './exercises.service';

@ApiBearerAuth()
@ApiTags('Exercise Library')
@Controller('exercises')
export class ExercisesController {
  constructor(private readonly service: ExercisesService) {}

  @RequirePermissions(Permission.ExercisesManage)
  @Post()
  create(@Body() dto: CreateExerciseDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.ExercisesRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.ExercisesRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.ExercisesManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateExerciseDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.ExercisesManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
