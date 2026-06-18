import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../shared/database/prisma.service';

@Injectable()
export class AuthRepository {
  constructor(private readonly prisma: PrismaService) {}

  findUserByEmail(email: string) {
    return (this.prisma as any).user.findUnique({
      where: { email },
      include: {
        credential: true,
        roles: { include: { role: { include: { permissions: { include: { permission: true } } } } } },
        branchAccess: true,
      },
    });
  }

  findUserById(id: string) {
    return (this.prisma as any).user.findUnique({
      where: { id },
      include: {
        roles: { include: { role: { include: { permissions: { include: { permission: true } } } } } },
        branchAccess: true,
      },
    });
  }

  async createUserWithCredential(data: { email: string; firstName: string; lastName: string; passwordHash: string; organizationId?: string; branchId?: string }) {
    return (this.prisma as any).$transaction(async (tx: any) => {
      const user = await tx.user.create({
        data: {
          email: data.email,
          firstName: data.firstName,
          lastName: data.lastName,
          organizationId: data.organizationId,
          status: 'active',
          credential: { create: { passwordHash: data.passwordHash, passwordUpdatedAt: new Date() } },
        },
      });
      if (data.organizationId && data.branchId) {
        await tx.userBranchAccess.create({ data: { userId: user.id, organizationId: data.organizationId, branchId: data.branchId, isPrimary: true } });
      }
      return user;
    });
  }

  createSession(data: Record<string, unknown>) {
    return (this.prisma as any).userSession.create({ data });
  }

  findSession(id: string) {
    return (this.prisma as any).userSession.findUnique({ where: { id } });
  }

  revokeSession(id: string) {
    return (this.prisma as any).userSession.update({ where: { id }, data: { revokedAt: new Date() } });
  }
}
