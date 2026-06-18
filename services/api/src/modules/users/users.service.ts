import { Injectable } from '@nestjs/common';
import { BaseCrudService } from '../../shared/database/base-crud.service';
import { CreateUserDto, UpdateUserDto } from './dto/users.dto';
import { UsersRepository } from './users.repository';

@Injectable()
export class UsersService extends BaseCrudService<CreateUserDto, UpdateUserDto> {
  constructor(protected readonly repository: UsersRepository) {
    super(repository);
  }
}
