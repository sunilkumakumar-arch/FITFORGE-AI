import { Controller, Get, Param } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { RequirePermissions } from '../auth/permissions.decorator';
import { MemberSummaryResponseDto } from './dto/members.dto';
import { MembersService } from './members.service';

@ApiBearerAuth()
@ApiTags('Member Summary')
@Controller('members')
export class MembersController {
  constructor(private readonly members: MembersService) {}

  @RequirePermissions('users.read')
  @Get(':id/summary')
  getSummary(@Param('id') id: string): Promise<MemberSummaryResponseDto> {
    return this.members.getSummary(id);
  }
}
