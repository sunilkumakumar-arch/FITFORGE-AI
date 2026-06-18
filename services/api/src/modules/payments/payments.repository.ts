import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreatePaymentDto, UpdatePaymentDto } from './dto/payments.dto';

@Injectable()
export class PaymentsRepository extends BaseRepository<CreatePaymentDto, UpdatePaymentDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'payment');
  }
}
