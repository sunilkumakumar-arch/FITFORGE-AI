import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsNumber, IsObject, IsOptional, IsString, IsUUID } from 'class-validator';
import { Type } from 'class-transformer';

export class CreatePostureDto {
  @ApiProperty()
  @IsUUID()
  organizationId!: string;

  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  branchId?: string;

  @ApiProperty()
  @IsUUID()
  memberId!: string;

  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  capturedBy?: string;

  @ApiProperty()
  @IsString()
  source!: string;

  @ApiProperty()
  @IsString()
  analysisType!: string;

  @ApiProperty()
  @Type(() => Number)
  @IsNumber()
  overallRiskScore!: number;

  @ApiProperty()
  @Type(() => Number)
  @IsNumber()
  confidenceScore!: number;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  summary?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  mediaUrl?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  reportUrl?: string;

  @ApiProperty()
  @IsString()
  modelVersion!: string;

  @ApiPropertyOptional()
  @IsObject()
  @IsOptional()
  consentSnapshot?: Record<string, unknown>;
}

export class UpdatePostureDto extends PartialType(CreatePostureDto) {}
