import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsArray, IsInt, IsOptional, IsString, IsUUID, Min } from 'class-validator';

export class CreateNutritionPlanDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() coachId?: string;
  @ApiProperty() @IsString() name!: string;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) calories!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(0) proteinGrams!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(0) carbsGrams!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(0) fatGrams!: number;
  @ApiPropertyOptional() @IsArray() @IsOptional() meals?: unknown[];
}

export class MacroCalculatorDto {
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) weightKg!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) heightCm!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(10) age!: number;
  @ApiProperty() @IsString() sex!: 'male' | 'female';
  @ApiProperty() @IsString() goal!: 'fat_loss' | 'maintenance' | 'muscle_gain';
}
