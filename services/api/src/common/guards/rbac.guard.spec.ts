import { ForbiddenException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { RbacGuard } from './rbac.guard';

describe('RbacGuard', () => {
  const reflector = { getAllAndOverride: jest.fn() } as unknown as Reflector;
  const guard = new RbacGuard(reflector);

  function context(user?: { permissions: string[] }) {
    return {
      getHandler: jest.fn(),
      getClass: jest.fn(),
      switchToHttp: () => ({ getRequest: () => ({ user }) }),
    } as any;
  }

  beforeEach(() => jest.clearAllMocks());

  it('allows public routes', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValueOnce(true);
    expect(guard.canActivate(context())).toBe(true);
  });

  it('allows users with all required permissions', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValueOnce(false).mockReturnValueOnce(['memberships.read']);
    expect(guard.canActivate(context({ permissions: ['memberships.read', 'attendance.read'] }))).toBe(true);
  });

  it('rejects users missing permissions', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValueOnce(false).mockReturnValueOnce(['audit.read']);
    expect(() => guard.canActivate(context({ permissions: ['memberships.read'] }))).toThrow(ForbiddenException);
  });
});
