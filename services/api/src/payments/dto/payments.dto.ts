import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsInt, IsObject, IsOptional, IsString, IsUUID, Min } from 'class-validator';

export class CreateRazorpayOrderDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() orderId?: string;
  @ApiProperty() @IsString() purpose!: 'membership_renewal' | 'pt_package' | 'product_purchase' | 'subscription';
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) amountMinor!: number;
  @ApiPropertyOptional({ default: 'INR' }) @IsString() @IsOptional() currency?: string;
  @ApiProperty() @IsString() idempotencyKey!: string;
  @ApiPropertyOptional() @IsObject() @IsOptional() metadata?: Record<string, unknown>;
}

export class RefundPaymentDto {
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) amountMinor!: number;
  @ApiPropertyOptional() @IsString() @IsOptional() reason?: string;
}
