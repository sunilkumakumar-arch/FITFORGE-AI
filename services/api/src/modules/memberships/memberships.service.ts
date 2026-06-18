import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateMembershipDto, UpdateMembershipDto } from './dto/memberships.dto';
import { MembershipsRepository } from './memberships.repository';

@Injectable()
export class MembershipsService extends BaseCrudService<CreateMembershipDto, UpdateMembershipDto> {
  constructor(protected readonly repository: MembershipsRepository) {
    super(repository);
  }
}
