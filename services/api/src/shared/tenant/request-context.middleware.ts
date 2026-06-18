import { Injectable, NestMiddleware } from '@nestjs/common';
import { randomUUID } from 'crypto';
import { Response, NextFunction } from 'express';
import { AuthenticatedRequest } from '../../common/interfaces/authenticated-request.interface';

@Injectable()
export class RequestContextMiddleware implements NestMiddleware {
  use(req: AuthenticatedRequest, res: Response, next: NextFunction) {
    const requestId = (req.headers['x-request-id'] as string | undefined) ?? randomUUID();
    req.context = {
      requestId,
      organizationId: req.headers['x-organization-id'] as string | undefined,
      branchId: req.headers['x-branch-id'] as string | undefined,
      ipAddress: req.ip,
      userAgent: req.headers['user-agent'],
    };
    res.setHeader('x-request-id', requestId);
    next();
  }
}
