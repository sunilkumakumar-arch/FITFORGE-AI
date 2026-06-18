import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsInt, IsObject, IsOptional, IsString, IsUUID } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateOrderDto {
  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  organizationId?: string;

  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  branchId?: string;

  @ApiProperty()
  @IsUUID()
  userId!: string;

  @ApiProperty()
  @IsString()
  orderNumber!: string;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  subtotalMinor!: number;

  @ApiPropertyOptional()
  @Type(() => Number)
  @IsInt()
  @IsOptional()
  taxMinor?: number;

  @ApiPropertyOptional()
  @Type(() => Number)
  @IsInt()
  @IsOptional()
  discountMinor?: number;

  @ApiPropertyOptional()
  @Type(() => Number)
  @IsInt()
  @IsOptional()
  shippingMinor?: number;

  @ApiProperty()
  @Type(() => Number)
  @IsInt()
  totalMinor!: number;

  @ApiProperty()
  @IsString()
  currency!: string;

  @ApiPropertyOptional()
  @IsObject()
  @IsOptional()
  shippingAddress?: Record<string, unknown>;

  @ApiPropertyOptional()
  @IsObject()
  @IsOptional()
  billingAddress?: Record<string, unknown>;
}

export class UpdateOrderDto extends PartialType(CreateOrderDto) {}
