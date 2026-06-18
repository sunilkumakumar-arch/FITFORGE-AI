import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateMembershipDto, UpdateMembershipDto } from './dto/memberships.dto';

@Injectable()
export class MembershipsRepository extends BaseRepository<CreateMembershipDto, UpdateMembershipDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'membership');
  }
}
