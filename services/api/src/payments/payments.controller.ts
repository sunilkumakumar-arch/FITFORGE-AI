import { Body, Controller, Headers, Post, Req } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { Public } from '../auth/public.decorator';
import { PaymentsService } from './payments.service';

@ApiBearerAuth()
@ApiTags('Razorpay Payments')
@Controller('payments')
export class PaymentsController {
  constructor(private readonly payments: PaymentsService) {}
  @Post('razorpay/orders') createOrder(@Body() dto: any) { return this.payments.createRazorpayOrder(dto); }
  @Public() @Post('razorpay/webhook') webhook(@Headers('x-razorpay-signature') signature: string, @Req() req: any, @Body() body: any) { return this.payments.handleWebhook(signature, JSON.stringify(body), body); }
}
