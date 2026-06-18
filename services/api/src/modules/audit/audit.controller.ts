import { Controller, Get, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { PrismaService } from '../../shared/database/prisma.service';

@ApiBearerAuth()
@ApiTags('Audit Logs')
@Controller('audit-logs')
export class AuditController {
  constructor(private readonly prisma: PrismaService) {}

  @RequirePermissions(Permission.AuditRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return (this.prisma as any).auditLog.findMany({
      skip: (query.page - 1) * query.limit,
      take: query.limit,
      orderBy: { createdAt: 'desc' },
    });
  }
}
