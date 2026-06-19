import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsInt, IsOptional, IsString, IsUUID, Min } from 'class-validator';

export class CreatePtPackageDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsString() name!: string;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) sessionCredits!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) validityDays!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) priceMinor!: number;
  @ApiPropertyOptional({ default: 'INR' }) @IsString() @IsOptional() currency?: string;
}

export class PurchasePtPackageDto {
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() trainerId?: string;
  @ApiProperty() @IsUUID() packageId!: string;
  @ApiProperty() @IsUUID() paymentId!: string;
}

export class ConsumePtCreditDto {
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() trainerId?: string;
  @ApiProperty() @IsUUID() bookingId!: string;
}
