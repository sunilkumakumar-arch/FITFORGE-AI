import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsArray, IsInt, IsObject, IsOptional, IsString, IsUUID } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateProductDto {
  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  organizationId?: string;

  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  vendorId?: string;

  @ApiProperty()
  @IsString()
  name!: string;

  @ApiProperty()
  @IsString()
  slug!: string;

  @ApiProperty()
  @IsString()
  category!: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  description?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  brand?: string;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  basePriceMinor!: number;

  @ApiProperty()
  @IsString()
  currency!: string;

  @ApiProperty()
  @IsArray()
  images!: string[];

  @ApiPropertyOptional()
  @IsObject()
  @IsOptional()
  attributes?: Record<string, unknown>;
}

export class UpdateProductDto extends PartialType(CreateProductDto) {}
