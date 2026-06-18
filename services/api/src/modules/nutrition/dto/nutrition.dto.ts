import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsArray, IsDateString, IsInt, IsOptional, IsString, IsUUID } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateNutritionDto {
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
  coachId?: string;

  @ApiProperty()
  @IsString()
  name!: string;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  calorieTarget!: number;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  proteinGrams!: number;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  carbsGrams!: number;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  fatGrams!: number;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  dietType?: string;

  @ApiProperty()
  @IsArray()
  allergies!: string[];

  @ApiPropertyOptional()
  @IsDateString()
  @IsOptional()
  startDate?: string;

  @ApiPropertyOptional()
  @IsDateString()
  @IsOptional()
  endDate?: string;
}

export class UpdateNutritionDto extends PartialType(CreateNutritionDto) {}
