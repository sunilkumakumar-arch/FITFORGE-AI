import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { IsOptional, IsString } from 'class-validator';

export class CreateOrganizationDto {
  @ApiProperty()
  @IsString()
  name!: string;

  @ApiProperty()
  @IsString()
  slug!: string;

  @ApiProperty()
  @IsString()
  type!: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  billingEmail?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  timezone?: string;
}

export class UpdateOrganizationDto extends PartialType(CreateOrganizationDto) {}
