import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../core/prisma.service';
import { SendWhatsappTemplateDto, WhatsappPreferenceDto } from './dto/whatsapp.dto';

@Injectable()
export class WhatsappService {
  constructor(private readonly config: ConfigService, private readonly prisma: PrismaService) {}

  async sendTemplate(dto: SendWhatsappTemplateDto) {
    const preference = await (this.prisma as any).notificationPreference.findUnique({ where: { phone_channel: { phone: dto.to, channel: 'whatsapp' } } }).catch(() => null);
    if (preference && !preference.enabled) {
      const message = await (this.prisma as any).notification.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, userId: dto.userId, channel: 'whatsapp', to: dto.to, template: dto.template, body: 'User opted out', status: 'failed' } });
      return { message, skipped: true, reason: 'recipient_opted_out' };
    }
    const phoneNumberId = this.config.get<string>('WHATSAPP_PHONE_NUMBER_ID');
    const url = `${this.config.get<string>('WHATSAPP_API_URL')}/${phoneNumberId}/messages`;
    const payload = { messaging_product: 'whatsapp', to: dto.to, type: 'template', template: { name: dto.template, language: { code: dto.language ?? 'en_US' }, components: dto.components ?? [] } };
    const response = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${this.config.get<string>('WHATSAPP_ACCESS_TOKEN')}`, 'content-type': 'application/json' }, body: JSON.stringify(payload) }).catch((error) => ({ ok: false, json: async () => ({ error: String(error) }) } as Response));
    const result = await response.json();
    const message = await (this.prisma as any).notification.create({ data: { organizationId: dto.organizationId, branchId: dto.branchId, userId: dto.userId, channel: 'whatsapp', to: dto.to, template: dto.template, body: JSON.stringify(payload), status: response.ok ? 'sent' : 'failed', providerId: result.messages?.[0]?.id } });
    return { message, providerResponse: result };
  }

  optIn(dto: WhatsappPreferenceDto) {
    return (this.prisma as any).notificationPreference.upsert({
      where: { phone_channel: { phone: dto.phone, channel: 'whatsapp' } },
      create: { organizationId: dto.organizationId, userId: dto.userId, phone: dto.phone, channel: 'whatsapp', enabled: true },
      update: { organizationId: dto.organizationId, userId: dto.userId, enabled: true },
    });
  }

  optOut(dto: WhatsappPreferenceDto) {
    return (this.prisma as any).notificationPreference.upsert({
      where: { phone_channel: { phone: dto.phone, channel: 'whatsapp' } },
      create: { organizationId: dto.organizationId, userId: dto.userId, phone: dto.phone, channel: 'whatsapp', enabled: false },
      update: { organizationId: dto.organizationId, userId: dto.userId, enabled: false },
    });
  }

  async handleWebhook(payload: any) {
    const statuses = payload?.entry?.flatMap((entry: any) => entry.changes ?? []).flatMap((change: any) => change.value?.statuses ?? []) ?? [];
    const updates = [];
    for (const status of statuses) {
      if (!status.id) continue;
      const mapped = status.status === 'read' ? 'read' : status.status === 'delivered' ? 'delivered' : status.status === 'failed' ? 'failed' : 'sent';
      updates.push(await (this.prisma as any).notification.updateMany({ where: { providerId: status.id }, data: { status: mapped } }));
    }
    return { processed: true, updates: updates.reduce((sum, item) => sum + item.count, 0) };
  }
}
