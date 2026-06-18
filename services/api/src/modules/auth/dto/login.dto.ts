import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsEmail, IsOptional, IsString } from 'class-validator';

export class LoginDto {
  @ApiProperty()
  @IsEmail()
  email!: string;

  @ApiProperty()
  @IsString()
  password!: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  deviceId?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  deviceName?: string;
}
