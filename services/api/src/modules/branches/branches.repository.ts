import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateBranchDto, UpdateBranchDto } from './dto/branches.dto';

@Injectable()
export class BranchesRepository extends BaseRepository<CreateBranchDto, UpdateBranchDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'branch');
  }
}
