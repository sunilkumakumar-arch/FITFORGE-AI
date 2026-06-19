import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Public } from '../auth/public.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { SendWhatsappTemplateDto, WhatsappPreferenceDto } from './dto/whatsapp.dto';
import { WhatsappService } from './whatsapp.service';

@ApiBearerAuth()
@ApiTags('WhatsApp Notifications')
@Controller('whatsapp')
export class WhatsappController {
  constructor(private readonly whatsapp: WhatsappService) {}

  @RequirePermissions('notifications.manage')
  @Post('send-template')
  sendTemplate(@Body() dto: SendWhatsappTemplateDto) { return this.whatsapp.sendTemplate(dto); }

  @Post('opt-in')
  optIn(@Body() dto: WhatsappPreferenceDto) { return this.whatsapp.optIn(dto); }

  @Post('opt-out')
  optOut(@Body() dto: WhatsappPreferenceDto) { return this.whatsapp.optOut(dto); }

  @Public()
  @Post('webhook')
  webhook(@Body() payload: any) { return this.whatsapp.handleWebhook(payload); }

  @Public()
  @Get('webhook')
  verifyWebhook(@Query('hub.challenge') challenge?: string) { return challenge ?? 'ok'; }
}
