import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateOrganizationDto, UpdateOrganizationDto } from './dto/organizations.dto';

@Injectable()
export class OrganizationsRepository extends BaseRepository<CreateOrganizationDto, UpdateOrganizationDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'organization');
  }
}
