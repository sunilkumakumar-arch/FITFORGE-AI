import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateOrganizationDto, UpdateOrganizationDto } from './dto/organizations.dto';
import { OrganizationsRepository } from './organizations.repository';

@Injectable()
export class OrganizationsService extends BaseCrudService<CreateOrganizationDto, UpdateOrganizationDto> {
  constructor(protected readonly repository: OrganizationsRepository) {
    super(repository);
  }
}
