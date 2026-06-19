import { Body, Controller, Get, Headers, Param, Post, Query, Req } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Public } from '../auth/public.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { CreateRazorpayOrderDto, RefundPaymentDto } from './dto/payments.dto';
import { PaymentsService } from './payments.service';

@ApiBearerAuth()
@ApiTags('Razorpay Payments')
@Controller('payments')
export class PaymentsController {
  constructor(private readonly payments: PaymentsService) {}

  @RequirePermissions('payments.manage')
  @Post('razorpay/orders')
  createOrder(@Body() dto: CreateRazorpayOrderDto) { return this.payments.createRazorpayOrder(dto); }

  @Public() @Post('razorpay/webhook') webhook(@Headers('x-razorpay-signature') signature: string, @Req() req: any, @Body() body: any) { return this.payments.handleWebhook(signature, JSON.stringify(body), body); }

  @RequirePermissions('payments.manage')
  @Post(':id/refund')
  refund(@Param('id') id: string, @Body() dto: RefundPaymentDto) { return this.payments.refundPayment(id, dto); }

  @RequirePermissions('payments.read')
  @Get()
  list(@Query() query: any) { return this.payments.list(query); }
}
