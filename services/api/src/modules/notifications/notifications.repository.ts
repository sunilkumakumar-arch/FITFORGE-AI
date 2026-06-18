import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateNotificationDto, UpdateNotificationDto } from './dto/notifications.dto';

@Injectable()
export class NotificationsRepository extends BaseRepository<CreateNotificationDto, UpdateNotificationDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'notification');
  }
}
