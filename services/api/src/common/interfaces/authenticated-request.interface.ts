import { Request } from 'express';

export interface JwtUser {
  sub: string;
  email: string;
  organizationId?: string | null;
  branchIds: string[];
  roleKeys: string[];
  permissions: string[];
}

export interface RequestContext {
  requestId?: string;
  organizationId?: string;
  branchId?: string;
  ipAddress?: string;
  userAgent?: string;
}

export interface AuthenticatedRequest extends Request {
  user?: JwtUser;
  context?: RequestContext;
}
