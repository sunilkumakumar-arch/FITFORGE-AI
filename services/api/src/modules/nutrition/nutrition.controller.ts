import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreateNutritionDto, UpdateNutritionDto } from './dto/nutrition.dto';
import { NutritionService } from './nutrition.service';

@ApiBearerAuth()
@ApiTags('Nutrition Planning')
@Controller('nutrition-plans')
export class NutritionController {
  constructor(private readonly service: NutritionService) {}

  @RequirePermissions(Permission.NutritionManage)
  @Post()
  create(@Body() dto: CreateNutritionDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.NutritionRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.NutritionRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.NutritionManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdateNutritionDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.NutritionManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
