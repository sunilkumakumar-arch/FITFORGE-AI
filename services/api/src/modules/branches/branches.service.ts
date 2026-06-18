import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateBranchDto, UpdateBranchDto } from './dto/branches.dto';
import { BranchesRepository } from './branches.repository';

@Injectable()
export class BranchesService extends BaseCrudService<CreateBranchDto, UpdateBranchDto> {
  constructor(protected readonly repository: BranchesRepository) {
    super(repository);
  }
}
