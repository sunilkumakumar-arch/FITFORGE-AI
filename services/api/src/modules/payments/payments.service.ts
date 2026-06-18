import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreatePaymentDto, UpdatePaymentDto } from './dto/payments.dto';
import { PaymentsRepository } from './payments.repository';

@Injectable()
export class PaymentsService extends BaseCrudService<CreatePaymentDto, UpdatePaymentDto> {
  constructor(protected readonly repository: PaymentsRepository) {
    super(repository);
  }

  createPaymentIntent(dto: CreatePaymentDto) {
    return this.create({ ...dto, metadata: { ...(dto.metadata ?? {}), integrationMode: 'provider_adapter_pending' } });
  }
}
