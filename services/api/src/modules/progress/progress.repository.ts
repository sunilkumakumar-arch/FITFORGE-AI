import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateProgresDto, UpdateProgresDto } from './dto/progress.dto';

@Injectable()
export class ProgressRepository extends BaseRepository<CreateProgresDto, UpdateProgresDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'progressEntry');
  }
}
