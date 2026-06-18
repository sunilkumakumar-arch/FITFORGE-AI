import { ApiPropertyOptional } from '@nestjs/swagger';
import { IsOptional, IsUUID } from 'class-validator';

export class TenantScopedDto {
  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  organizationId?: string;

  @ApiPropertyOptional()
  @IsUUID()
  @IsOptional()
  branchId?: string;
}
