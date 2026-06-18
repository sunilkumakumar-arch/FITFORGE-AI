import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../core/prisma.service';

@Injectable()
export class WhatsappService {
  constructor(private readonly config: ConfigService, private readonly prisma: PrismaService) {}
  async sendTemplate(dto: any) {
    const phoneNumberId = this.config.get<string>('WHATSAPP_PHONE_NUMBER_ID');
    const url = `${this.config.get<string>('WHATSAPP_API_URL')}/${phoneNumberId}/messages`;
    const payload = { messaging_product: 'whatsapp', to: dto.to, type: 'template', template: { name: dto.template, language: { code: dto.language ?? 'en_US' }, components: dto.components ?? [] } };
    const response = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${this.config.get<string>('WHATSAPP_ACCESS_TOKEN')}`, 'content-type': 'application/json' }, body: JSON.stringify(payload) }).catch((error) => ({ ok: false, json: async () => ({ error: String(error) }) } as Response));
    const result = await response.json();
    const message = await (this.prisma as any).notification.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, userId: dto.userId, channel: 'whatsapp', to: dto.to, template: dto.template, body: JSON.stringify(payload), status: response.ok ? 'sent' : 'failed', providerId: result.messages?.[0]?.id } });
    return { message, providerResponse: result };
  }
}
