import { CanActivate, ExecutionContext, HttpException, HttpStatus, Injectable } from '@nestjs/common';

interface Bucket { count: number; resetAt: number; }

@Injectable()
export class RateLimitGuard implements CanActivate {
  private readonly buckets = new Map<string, Bucket>();
  private readonly limit = Number(process.env.RATE_LIMIT_PER_MINUTE ?? 120);
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const key = request.user?.sub ?? request.ip ?? 'anonymous';
    const now = Date.now();
    const current = this.buckets.get(key);
    if (!current || current.resetAt < now) { this.buckets.set(key, { count: 1, resetAt: now + 60_000 }); return true; }
    current.count += 1;
    if (current.count > this.limit) throw new HttpException('Rate limit exceeded', HttpStatus.TOO_MANY_REQUESTS);
    return true;
  }
}
