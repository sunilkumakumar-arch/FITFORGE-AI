import { UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import { Test } from '@nestjs/testing';
import * as bcrypt from 'bcryptjs';
import { AuditService } from '../audit/audit.service';
import { AuthRepository } from './auth.repository';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  const repository = {
    findUserByEmail: jest.fn(),
    findUserById: jest.fn(),
    createUserWithCredential: jest.fn(),
    createSession: jest.fn(),
    findSession: jest.fn(),
    revokeSession: jest.fn(),
    prisma: { userSession: { update: jest.fn() } },
  };
  const jwt = { signAsync: jest.fn(), verifyAsync: jest.fn() };
  const config = { get: jest.fn((key: string) => ({ BCRYPT_ROUNDS: '4', JWT_ACCESS_EXPIRES_IN: '15m', JWT_REFRESH_EXPIRES_IN: '30d' }[key])) };
  const audit = { record: jest.fn() };

  let service: AuthService;

  beforeEach(async () => {
    jest.clearAllMocks();
    const moduleRef = await Test.createTestingModule({
      providers: [
        AuthService,
        { provide: AuthRepository, useValue: repository },
        { provide: JwtService, useValue: jwt },
        { provide: AuditService, useValue: audit },
        { provide: ConfigService, useValue: config },
      ],
    })
      .overrideProvider(JwtService)
      .useValue(jwt)
      .overrideProvider(ConfigService)
      .useValue(config)
      .compile();

    service = moduleRef.get(AuthService);
  });

  it('rejects invalid login credentials', async () => {
    repository.findUserByEmail.mockResolvedValue(null);
    await expect(service.login({ email: 'member@example.com', password: 'bad' })).rejects.toBeInstanceOf(UnauthorizedException);
  });

  it('issues access and refresh tokens for a valid login', async () => {
    const hash = await bcrypt.hash('valid-password', 4);
    const user = {
      id: 'user-1',
      email: 'member@example.com',
      organizationId: 'org-1',
      credential: { passwordHash: hash },
      roles: [{ role: { systemKey: 'member', permissions: [{ permission: { key: 'progress.read' } }] } }],
      branchAccess: [{ branchId: 'branch-1' }],
    };
    repository.findUserByEmail.mockResolvedValue(user);
    repository.findUserById.mockResolvedValue(user);
    repository.createSession.mockResolvedValue({ id: 'session-1' });
    jwt.signAsync.mockResolvedValueOnce('access-token').mockResolvedValueOnce('refresh-token');

    const result = await service.login({ email: user.email, password: 'valid-password' });

    expect(result).toMatchObject({ accessToken: 'access-token', refreshToken: 'refresh-token', tokenType: 'Bearer' });
    expect(repository.prisma.userSession.update).toHaveBeenCalledWith(expect.objectContaining({ where: { id: 'session-1' } }));
  });
});
