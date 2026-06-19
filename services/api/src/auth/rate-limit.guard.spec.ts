import { HttpException, HttpStatus } from '@nestjs/common';
import { RateLimitGuard } from './rate-limit.guard';

describe('RateLimitGuard', () => {
  it('rejects requests above configured limit', () => {
    process.env.RATE_LIMIT_PER_MINUTE = '1';
    const guard = new RateLimitGuard();
    const context: any = { switchToHttp: () => ({ getRequest: () => ({ ip: '1.1.1.1' }) }) };
    expect(guard.canActivate(context)).toBe(true);
    expect(() => guard.canActivate(context)).toThrow(HttpException);
    try {
      guard.canActivate(context);
    } catch (error) {
      expect((error as HttpException).getStatus()).toBe(HttpStatus.TOO_MANY_REQUESTS);
    }
  });
});
