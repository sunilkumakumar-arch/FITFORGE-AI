import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsArray, IsObject, IsOptional, IsString, IsUUID } from 'class-validator';

export class SendWhatsappTemplateDto {
  @ApiPropertyOptional() @IsUUID() @IsOptional() organizationId?: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() branchId?: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() userId?: string;
  @ApiProperty() @IsString() to!: string;
  @ApiProperty() @IsString() template!: string;
  @ApiPropertyOptional({ default: 'en_US' }) @IsString() @IsOptional() language?: string;
  @ApiPropertyOptional() @IsArray() @IsOptional() components?: unknown[];
}

export class WhatsappPreferenceDto {
  @ApiPropertyOptional() @IsUUID() @IsOptional() organizationId?: string;
  @ApiPropertyOptional() @IsUUID() @IsOptional() userId?: string;
  @ApiProperty() @IsString() phone!: string;
}

export class WhatsappWebhookDto {
  @ApiProperty() @IsObject() payload!: Record<string, unknown>;
}
