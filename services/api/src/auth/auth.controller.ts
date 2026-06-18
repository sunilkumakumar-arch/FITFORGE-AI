import { Body, Controller, Get, Post } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { Public } from './public.decorator';
import { CurrentUser } from './current-user.decorator';
import { AuthUser } from './auth.types';

@ApiTags('Authentication')
@Controller('auth')
export class AuthController {
  constructor(private readonly auth: AuthService) {}
  @Public() @Post('register') register(@Body() dto: any) { return this.auth.register(dto); }
  @Public() @Post('login') login(@Body() dto: any) { return this.auth.login(dto); }
  @Public() @Post('refresh-token') refresh(@Body('refreshToken') token: string) { return this.auth.refresh(token); }
  @ApiBearerAuth() @Get('me') me(@CurrentUser() user: AuthUser) { return this.auth.me(user.sub); }
}
