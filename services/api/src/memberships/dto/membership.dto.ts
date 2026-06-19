import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsBoolean, IsDateString, IsInt, IsOptional, IsString, IsUUID, Min } from 'class-validator';

export class CreateMembershipPlanDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiProperty() @IsString() name!: string;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(1) durationDays!: number;
  @ApiProperty() @Type(() => Number) @IsInt() @Min(0) priceMinor!: number;
  @ApiPropertyOptional({ default: 'INR' }) @IsString() @IsOptional() currency?: string;
}

export class UpdateMembershipPlanDto extends PartialType(CreateMembershipPlanDto) {
  @ApiPropertyOptional() @IsBoolean() @IsOptional() isActive?: boolean;
}

export class CreateMembershipDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiProperty() @IsUUID() planId!: string;
  @ApiPropertyOptional() @IsDateString() @IsOptional() startDate?: string;
  @ApiPropertyOptional() @IsDateString() @IsOptional() endDate?: string;
  @ApiPropertyOptional() @IsBoolean() @IsOptional() autoRenew?: boolean;
  @ApiPropertyOptional() @IsBoolean() @IsOptional() activateImmediately?: boolean;
}

export class RenewMembershipDto {
  @ApiPropertyOptional() @IsUUID() @IsOptional() planId?: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() paymentId?: string;
  @ApiPropertyOptional() @IsBoolean() @IsOptional() activateImmediately?: boolean;
}

export class MembershipStatusDto {
  @ApiProperty() @IsString() status!: 'active' | 'paused' | 'cancelled' | 'expired';
}
