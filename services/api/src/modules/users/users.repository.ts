import { Injectable } from '@nestjs/common';
import { BaseRepository } from '../../shared/database/base.repository';
import { PrismaService } from '../../shared/database/prisma.service';
import { CreateUserDto, UpdateUserDto } from './dto/users.dto';

@Injectable()
export class UsersRepository extends BaseRepository<CreateUserDto, UpdateUserDto> {
  constructor(prisma: PrismaService) {
    super(prisma, 'user');
  }
}
