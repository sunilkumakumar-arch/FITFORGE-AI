import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsArray, IsOptional, IsString, IsUUID } from 'class-validator';

export class CreateExerciseDto {
  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  organizationId?: string;

  @ApiProperty()
  @IsString()
  name!: string;

  @ApiProperty()
  @IsString()
  slug!: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  description?: string;

  @ApiProperty()
  @IsString()
  primaryMuscleGroup!: string;

  @ApiProperty()
  @IsArray()
  secondaryMuscleGroups!: string[];

  @ApiProperty()
  @IsArray()
  equipment!: string[];

  @ApiProperty()
  @IsString()
  difficulty!: string;

  @ApiProperty()
  @IsString()
  instructions!: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  safetyInstructions?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  commonMistakes?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  coachingTips?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  imageUrl?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  videoUrl?: string;
}

export class UpdateExerciseDto extends PartialType(CreateExerciseDto) {}
