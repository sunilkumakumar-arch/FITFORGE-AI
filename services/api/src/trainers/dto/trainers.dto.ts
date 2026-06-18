import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsDateString, IsOptional, IsString, IsUUID } from 'class-validator';

export class CreateTrainerAvailabilityDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiProperty() @IsUUID() trainerId!: string;
  @ApiProperty() @IsDateString() startsAt!: string;
  @ApiProperty() @IsDateString() endsAt!: string;
}

export class CreateTrainerBookingDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiProperty() @IsUUID() trainerId!: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiProperty() @IsDateString() startsAt!: string;
  @ApiProperty() @IsDateString() endsAt!: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() paymentId?: string;
}

export class BookingStatusDto { @ApiProperty() @IsString() status!: 'confirmed' | 'completed' | 'cancelled' | 'no_show'; }
