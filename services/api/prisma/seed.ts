import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcryptjs';

const prisma = new PrismaClient();
const permissions = [
  'organizations.read','organizations.manage','branches.read','branches.manage','users.read','users.manage','roles.read','roles.manage',
  'memberships.read','memberships.manage','memberships.renew','attendance.read','attendance.manage','attendance.check_in',
  'workouts.read','workouts.manage','nutrition.read','nutrition.manage','products.read','products.manage','inventory.read','inventory.manage',
  'orders.read','orders.manage','payments.read','payments.manage','notifications.read','notifications.manage','bookings.read','bookings.manage','posture.read','posture.manage','audit.read'
];
const adminPermissions = permissions;
const memberPermissions = ['memberships.read','attendance.check_in','attendance.read','workouts.read','nutrition.read','products.read','orders.read','payments.read','notifications.read','posture.read','posture.manage'];
const trainerPermissions = ['users.read','workouts.read','workouts.manage','nutrition.read','nutrition.manage','bookings.read','bookings.manage','posture.read','posture.manage'];

async function main() {
  const org = await prisma.organization.upsert({ where: { slug: 'fitforge-demo' }, update: {}, create: { name: 'FITFORGE Demo', slug: 'fitforge-demo' } });
  const branch = await prisma.branch.upsert({ where: { organizationId_code: { organizationId: org.id, code: 'HQ' } }, update: {}, create: { organizationId: org.id, name: 'Headquarters', code: 'HQ', city: 'Bengaluru' } });
  for (const key of permissions) await prisma.permission.upsert({ where: { key }, update: {}, create: { key, description: key } });
  const adminRole = await upsertRole(org.id, 'Admin', 'admin', adminPermissions);
  await upsertRole(org.id, 'Trainer', 'trainer', trainerPermissions);
  await upsertRole(org.id, 'Member', 'member', memberPermissions);
  const passwordHash = await bcrypt.hash('Fitforge@12345', 12);
  const admin = await prisma.user.upsert({ where: { email: 'admin@fitforge.ai' }, update: {}, create: { organizationId: org.id, email: 'admin@fitforge.ai', firstName: 'FITFORGE', lastName: 'Admin', credential: { create: { passwordHash } } } });
  const existingAdminRole = await prisma.userRole.findFirst({ where: { userId: admin.id, roleId: adminRole.id, branchId: branch.id } });
  if (!existingAdminRole) {
    await prisma.userRole.create({ data: { userId: admin.id, roleId: adminRole.id, branchId: branch.id } });
  }
  const plan = await prisma.membershipPlan.create({ data: { organizationId: org.id, branchId: branch.id, name: 'Demo Monthly', durationDays: 30, priceMinor: 299900 } }).catch(() => null);
  console.log({ organizationId: org.id, branchId: branch.id, adminEmail: admin.email, planId: plan?.id });
}
async function upsertRole(organizationId: string, name: string, key: any, permissionKeys: string[]) {
  const role = await prisma.role.upsert({ where: { organizationId_key: { organizationId, key } }, update: { name }, create: { organizationId, name, key } });
  const perms = await prisma.permission.findMany({ where: { key: { in: permissionKeys } } });
  for (const permission of perms) await prisma.rolePermission.upsert({ where: { roleId_permissionId: { roleId: role.id, permissionId: permission.id } }, update: {}, create: { roleId: role.id, permissionId: permission.id } });
  return role;
}
main().finally(() => prisma.$disconnect());
