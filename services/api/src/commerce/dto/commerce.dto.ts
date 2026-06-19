import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsArray, IsInt, IsOptional, IsString, IsUUID, Min } from 'class-validator';

export class CreateProductDto {
  @ApiPropertyOptional() @IsUUID() @IsOptional() organizationId?: string;
  @ApiProperty() @IsString() name!: string;
  @ApiProperty() @IsString() slug!: string;
  @ApiProperty() @IsString() category!: 'apparel' | 'footwear' | 'accessory' | 'equipment' | 'supplement';
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) priceMinor!: number;
  @ApiPropertyOptional({ default: 'INR' }) @IsString() @IsOptional() currency?: string;
}

export class UpsertInventoryDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiProperty() @IsUUID() productId!: string;
  @ApiProperty() @IsString() sku!: string;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(0) quantityAvailable!: number;
  @ApiPropertyOptional() @Type(() => Number) @IsInt() @Min(0) @IsOptional() reorderThreshold?: number;
}

export class AddCartItemDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsUUID() userId!: string;
  @ApiProperty() @IsUUID() productId!: string;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) quantity!: number;
}

export class CheckoutDto {
  @ApiProperty() @IsUUID() userId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiPropertyOptional() @IsArray() @IsOptional() metadata?: unknown[];
}
