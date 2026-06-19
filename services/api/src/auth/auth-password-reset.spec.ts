import { AuthService } from './auth.service';

describe('AuthService password reset', () => {
  it('returns success without leaking unknown emails', async () => {
    const prisma: any = { user: { findUnique: jest.fn().mockResolvedValue(null) } };
    const service = new AuthService(prisma, {} as any, {} as any, { log: jest.fn() } as any);
    await expect(service.requestPasswordReset('missing@example.com')).resolves.toEqual({ success: true });
  });
});
