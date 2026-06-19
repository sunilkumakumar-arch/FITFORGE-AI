import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { CreateExerciseDto, CreateWorkoutProgramDto } from './dto/workouts.dto';
import { WorkoutsService } from './workouts.service';

@ApiBearerAuth()
@ApiTags('Workout Management')
@Controller()
export class WorkoutsController {
  constructor(private readonly workouts: WorkoutsService) {}
  @RequirePermissions('workouts.manage') @Post('exercises') createExercise(@Body() dto: CreateExerciseDto) { return this.workouts.createExercise(dto); }
  @RequirePermissions('workouts.read') @Get('exercises') listExercises(@Query() query: any) { return this.workouts.listExercises(query); }
  @RequirePermissions('workouts.manage') @Post('workout-programs') createProgram(@Body() dto: CreateWorkoutProgramDto, @CurrentUser() user: any) { return this.workouts.createProgram(dto, user?.sub); }
  @RequirePermissions('workouts.read') @Get('workout-programs') listPrograms(@Query() query: any) { return this.workouts.listPrograms(query); }
}
