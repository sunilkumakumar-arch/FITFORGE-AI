import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { AnalyzePostureFrameDto, CreateBodyMeasurementDto } from './dto/posture.dto';
import { PostureService } from './posture.service';

@ApiBearerAuth()
@ApiTags('AI Posture Analysis')
@Controller('posture')
export class PostureController {
  constructor(private readonly posture: PostureService) {}
  @RequirePermissions('posture.manage') @Post('analyze-frame') analyzeFrame(@Body() dto: AnalyzePostureFrameDto, @CurrentUser() user: any) { return this.posture.analyzeFrame(dto, user?.sub); }
  @RequirePermissions('posture.read') @Get('sessions') listSessions(@Query() query: any) { return this.posture.listSessions(query); }
  @RequirePermissions('posture.manage') @Post('body-measurements') createBodyMeasurement(@Body() dto: CreateBodyMeasurementDto) { return this.posture.createBodyMeasurement(dto); }
}
