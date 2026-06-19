import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CurrentUser } from '../auth/current-user.decorator';
import { RequirePermissions } from '../auth/permissions.decorator';
import { CommerceService } from './commerce.service';
import { AddCartItemDto, CheckoutDto, CreateProductDto, UpsertInventoryDto } from './dto/commerce.dto';

@ApiBearerAuth()
@ApiTags('Inventory and E-commerce')
@Controller()
export class CommerceController {
  constructor(private readonly commerce: CommerceService) {}
  @RequirePermissions('products.manage') @Post('products') createProduct(@Body() dto: CreateProductDto) { return this.commerce.createProduct(dto); }
  @RequirePermissions('products.read') @Get('products') listProducts(@Query() query: any) { return this.commerce.listProducts(query); }
  @RequirePermissions('inventory.manage') @Post('inventory') upsertInventory(@Body() dto: UpsertInventoryDto) { return this.commerce.upsertInventory(dto); }
  @RequirePermissions('inventory.read') @Get('inventory') listInventory(@Query() query: any) { return this.commerce.listInventory(query); }
  @RequirePermissions('orders.manage') @Post('cart/items') addCartItem(@Body() dto: AddCartItemDto) { return this.commerce.addCartItem(dto); }
  @RequirePermissions('orders.read') @Get('cart/:userId') getCart(@Param('userId') userId: string) { return this.commerce.getCart(userId); }
  @RequirePermissions('orders.manage') @Post('checkout') checkout(@Body() dto: CheckoutDto, @CurrentUser() user: any) { return this.commerce.checkout(dto, user?.sub); }
  @RequirePermissions('orders.manage') @Post('orders/:id/fulfill') fulfill(@Param('id') id: string, @CurrentUser() user: any) { return this.commerce.fulfillOrder(id, user?.sub); }
}
