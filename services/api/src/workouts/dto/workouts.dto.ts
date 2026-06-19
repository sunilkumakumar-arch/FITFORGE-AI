import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsArray, IsOptional, IsString, IsUUID } from 'class-validator';

export class CreateExerciseDto {
  @ApiPropertyOptional() @IsUUID() @IsOptional() organizationId?: string;
  @ApiProperty() @IsString() name!: string;
  @ApiProperty() @IsString() slug!: string;
  @ApiProperty({ type: [String] }) @IsArray() muscleGroups!: string[];
  @ApiProperty() @IsString() difficulty!: string;
  @ApiProperty() @IsString() instructions!: string;
  @ApiPropertyOptional() @IsString() @IsOptional() videoUrl?: string;
}

export class CreateWorkoutProgramDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() trainerId?: string;
  @ApiProperty() @IsString() name!: string;
  @ApiProperty() @IsString() goal!: string;
  @ApiPropertyOptional() @IsArray() @IsOptional() exercises?: unknown[];
}
