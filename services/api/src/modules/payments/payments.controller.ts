import { Body, Controller, Delete, Get, Param, ParseUUIDPipe, Patch, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Permission } from '../../common/constants/permissions';
import { RequirePermissions } from '../../common/decorators/permissions.decorator';
import { Public } from '../../common/decorators/public.decorator';
import { PaginationQueryDto } from '../../common/dto/pagination-query.dto';
import { CreatePaymentDto, UpdatePaymentDto } from './dto/payments.dto';
import { PaymentsService } from './payments.service';

@ApiBearerAuth()
@ApiTags('Payment Integration Layer')
@Controller('payments')
export class PaymentsController {
  constructor(private readonly service: PaymentsService) {}

  @RequirePermissions(Permission.PaymentsManage)
  @Post()
  create(@Body() dto: CreatePaymentDto) {
    return this.service.create(dto);
  }

  @RequirePermissions(Permission.PaymentsManage)
  @Post('intent')
  createPaymentIntent(@Body() dto: CreatePaymentDto) {
    return this.service.createPaymentIntent(dto);
  }

  @Public()
  @Post('webhook/:provider')
  webhook(@Param('provider') provider: string, @Body() payload: Record<string, unknown>) {
    return { received: true, provider, payloadType: typeof payload };
  }

  @RequirePermissions(Permission.PaymentsRead)
  @Get()
  findAll(@Query() query: PaginationQueryDto) {
    return this.service.findAll(query);
  }

  @RequirePermissions(Permission.PaymentsRead)
  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }

  @RequirePermissions(Permission.PaymentsManage)
  @Patch(':id')
  update(@Param('id', ParseUUIDPipe) id: string, @Body() dto: UpdatePaymentDto) {
    return this.service.update(id, dto);
  }

  @RequirePermissions(Permission.PaymentsManage)
  @Delete(':id')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.remove(id);
  }
}
