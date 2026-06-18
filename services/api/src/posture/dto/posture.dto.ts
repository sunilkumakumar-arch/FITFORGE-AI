import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsArray, IsObject, IsOptional, IsString, IsUUID } from 'class-validator';

export class AnalyzePostureFrameDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() capturedBy?: string;
  @ApiProperty() @IsString() exerciseType!: 'squat' | 'deadlift' | 'bench_press' | 'shoulder_press' | 'lunge' | 'plank';
  @ApiProperty({ type: Array }) @IsArray() landmarks!: Array<{ name: string; x: number; y: number; z?: number; visibility?: number }>;
}

export class CreateBodyMeasurementDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional() @IsString() @IsOptional() source?: string;
  @ApiPropertyOptional() @IsObject() @IsOptional() measurements?: Record<string, number>;
}
