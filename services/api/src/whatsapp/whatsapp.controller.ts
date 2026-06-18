import { Body, Controller, Post } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { WhatsappService } from './whatsapp.service';

@ApiBearerAuth()
@ApiTags('WhatsApp Notifications')
@Controller('whatsapp')
export class WhatsappController {
  constructor(private readonly whatsapp: WhatsappService) {}
  @Post('send-template') sendTemplate(@Body() dto: any) { return this.whatsapp.sendTemplate(dto); }
}
