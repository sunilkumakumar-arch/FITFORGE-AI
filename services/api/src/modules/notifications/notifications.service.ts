import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateNotificationDto, UpdateNotificationDto } from './dto/notifications.dto';
import { NotificationsRepository } from './notifications.repository';

@Injectable()
export class NotificationsService extends BaseCrudService<CreateNotificationDto, UpdateNotificationDto> {
  constructor(protected readonly repository: NotificationsRepository) {
    super(repository);
  }
}
