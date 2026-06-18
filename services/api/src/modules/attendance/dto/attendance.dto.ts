import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsDateString, IsOptional, IsString, IsUUID } from 'class-validator';

export class CreateAttendanceDto {
  @ApiProperty()
  @IsUUID()
  organizationId!: string;

  @ApiProperty()
  @IsUUID()
  branchId!: string;

  @ApiProperty()
  @IsUUID()
  memberId!: string;

  @ApiProperty()
  @IsString()
  method!: string;

  @ApiProperty()
  @IsDateString()
  checkInAt!: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  deviceId?: string;
}

export class UpdateAttendanceDto extends PartialType(CreateAttendanceDto) {}
