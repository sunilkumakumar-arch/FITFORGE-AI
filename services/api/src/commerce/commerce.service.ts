import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { AuditService } from '../core/audit.service';
import { PrismaService } from '../core/prisma.service';
import { AddCartItemDto, CheckoutDto, CreateProductDto, UpsertInventoryDto } from './dto/commerce.dto';

@Injectable()
export class CommerceService {
  constructor(private readonly prisma: PrismaService, private readonly audit: AuditService) {}

  createProduct(dto: CreateProductDto) { return (this.prisma as any).product.create({ data: { ...dto, currency: dto.currency ?? 'INR' } }); }
  listProducts(query: any) { return (this.prisma as any).product.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.category ? { category: query.category } : {}), isActive: true }, orderBy: { createdAt: 'desc' } }); }

  upsertInventory(dto: UpsertInventoryDto) {
    return (this.prisma as any).inventoryItem.upsert({
      where: { branchId_sku: { branchId: dto.branchId, sku: dto.sku } },
      create: { ...dto, reorderThreshold: dto.reorderThreshold ?? 0 },
      update: { productId: dto.productId, quantityAvailable: dto.quantityAvailable, reorderThreshold: dto.reorderThreshold ?? 0 },
    });
  }
  listInventory(query: any) { return (this.prisma as any).inventoryItem.findMany({ where: { ...(query.organizationId ? { organizationId: query.organizationId } : {}), ...(query.branchId ? { branchId: query.branchId } : {}) }, include: { product: true }, orderBy: { updatedAt: 'desc' } }); }

  async addCartItem(dto: AddCartItemDto) {
    const product = await (this.prisma as any).product.findUnique({ where: { id: dto.productId } });
    if (!product || !product.isActive) throw new NotFoundException('Active product not found');
    const cart = await (this.prisma as any).cart.upsert({ where: { userId: dto.userId }, create: { organizationId: dto.organizationId, branchId: dto.branchId, userId: dto.userId }, update: { organizationId: dto.organizationId, branchId: dto.branchId } });
    return (this.prisma as any).cartItem.upsert({ where: { cartId_productId: { cartId: cart.id, productId: dto.productId } }, create: { cartId: cart.id, productId: dto.productId, quantity: dto.quantity, unitPriceMinor: product.priceMinor }, update: { quantity: { increment: dto.quantity }, unitPriceMinor: product.priceMinor } });
  }

  getCart(userId: string) { return (this.prisma as any).cart.findUnique({ where: { userId }, include: { items: { include: { product: true } } } }); }

  async checkout(dto: CheckoutDto, actorUserId?: string) {
    const cart = await this.getCart(dto.userId);
    if (!cart?.items?.length) throw new BadRequestException('Cart is empty');
    const branchId = dto.branchId ?? cart.branchId;
    if (!branchId) throw new BadRequestException('Branch is required for inventory reservation');
    const totalMinor = cart.items.reduce((sum: number, item: any) => sum + item.quantity * item.unitPriceMinor, 0);
    return (this.prisma as any).$transaction(async (tx: any) => {
      for (const item of cart.items) {
        const inventory = await tx.inventoryItem.findFirst({ where: { branchId, productId: item.productId } });
        if (!inventory || inventory.quantityAvailable - inventory.quantityReserved < item.quantity) throw new BadRequestException(`Insufficient stock for ${item.product.name}`);
      }
      const order = await tx.order.create({ data: { organizationId: cart.organizationId, branchId, userId: dto.userId, orderNumber: `ORD-${Date.now()}`, items: cart.items.map((item: any) => ({ productId: item.productId, name: item.product.name, quantity: item.quantity, unitPriceMinor: item.unitPriceMinor })), totalMinor } });
      for (const item of cart.items) {
        const inventory = await tx.inventoryItem.findFirst({ where: { branchId, productId: item.productId } });
        await tx.inventoryItem.update({ where: { id: inventory.id }, data: { quantityReserved: { increment: item.quantity } } });
        await tx.inventoryReservation.create({ data: { organizationId: cart.organizationId, branchId, inventoryItemId: inventory.id, orderId: order.id, quantity: item.quantity, expiresAt: new Date(Date.now() + 15 * 60 * 1000) } });
      }
      await tx.cartItem.deleteMany({ where: { cartId: cart.id } });
      await this.audit.log({ action: 'commerce.checkout', entityType: 'order', entityId: order.id, actorUserId, organizationId: order.organizationId, branchId: order.branchId, afterData: order });
      return order;
    });
  }

  async fulfillOrder(orderId: string, actorUserId?: string) {
    return (this.prisma as any).$transaction(async (tx: any) => {
      const order = await tx.order.findUnique({ where: { id: orderId } });
      if (!order) throw new NotFoundException('Order not found');
      const reservations = await tx.inventoryReservation.findMany({ where: { orderId, status: 'active' } });
      for (const reservation of reservations) {
        await tx.inventoryItem.update({ where: { id: reservation.inventoryItemId }, data: { quantityAvailable: { decrement: reservation.quantity }, quantityReserved: { decrement: reservation.quantity } } });
        await tx.inventoryReservation.update({ where: { id: reservation.id }, data: { status: 'fulfilled', releasedAt: new Date() } });
      }
      const updated = await tx.order.update({ where: { id: orderId }, data: { status: 'fulfilled' } });
      await this.audit.log({ action: 'commerce.fulfill_order', entityType: 'order', entityId: orderId, actorUserId, organizationId: updated.organizationId, branchId: updated.branchId });
      return updated;
    });
  }
}
