import { CanActivate, ExecutionContext, ForbiddenException, Injectable } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { PERMISSIONS } from './permissions.decorator';
import { IS_PUBLIC } from './public.decorator';

@Injectable()
export class RbacGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}
  canActivate(context: ExecutionContext): boolean {
    if (this.reflector.getAllAndOverride<boolean>(IS_PUBLIC, [context.getHandler(), context.getClass()])) return true;
    const required = this.reflector.getAllAndOverride<string[]>(PERMISSIONS, [context.getHandler(), context.getClass()]) ?? [];
    if (required.length === 0) return true;
    const user = context.switchToHttp().getRequest().user;
    if (!user || !required.every((p) => user.permissions?.includes(p))) throw new ForbiddenException('Insufficient permissions');
    return true;
  }
}
