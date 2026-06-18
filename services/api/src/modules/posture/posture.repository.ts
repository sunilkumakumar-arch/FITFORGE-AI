import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreatePostureDto, UpdatePostureDto } from './dto/posture.dto';

@Injectable()
export class PostureRepository extends BaseRepository<CreatePostureDto, UpdatePostureDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'postureSession');
  }
}
