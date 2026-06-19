import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsInt, IsOptional, IsString, IsUUID, Min } from 'class-validator';

export class CreateQrTokenDto {
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiPropertyOptional({ default: 300 }) @Type(() => Number) @IsInt() @Min(30) @IsOptional() ttlSeconds?: number;
}

export class QrCheckInDto {
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiProperty() @IsString() token!: string;
  @ApiPropertyOptional() @IsString() @IsOptional() deviceId?: string;
}

export class ManualCheckInDto {
  @ApiProperty() @IsUUID() organizationId!: string;
  @ApiProperty() @IsUUID() branchId!: string;
  @ApiProperty() @IsUUID() memberId!: string;
  @ApiPropertyOptional({ default: 'manual' }) @IsString() @IsOptional() method?: 'manual' | 'mobile' | 'biometric';
  @ApiPropertyOptional() @IsString() @IsOptional() deviceId?: string;
}
