# FITFORGE-AI
AI-powered fitness ecosystem

## Phase 8 Production Implementation

Runnable applications:

- `services/api` - NestJS backend APIs with Prisma, JWT auth, RBAC, memberships, attendance, workouts, nutrition, inventory, e-commerce, QR attendance, Razorpay, and WhatsApp integrations.
- `apps/admin-web` - Next.js admin dashboard for commercial operations.
- `apps/mobile` - Flutter mobile app source for members and trainers.

## Commands

```bash
npm install
npm run api:prisma:validate
npm run api:build
npm run api:test
npm run web:typecheck
npm run web:build
```

Flutter SDK is required locally for mobile validation:

```bash
cd apps/mobile
flutter create --platforms=android,ios .
flutter analyze
```

## Deployment

- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Project Status](PROJECT_STATUS.md)

## Phase Documents

- [Phase 3: PostgreSQL Database Schema](docs/phase-03-postgresql-database-schema.md)
- [Phase 6: AI Posture and Computer Vision](docs/phase-06-ai-posture-computer-vision.md)
- [Phase 7: Production Deployment, Security, Payments, and Commercial Readiness](docs/phase-07-production-deployment-security-payments-readiness.md)
- [Phase 9: Production Feature Implementation](docs/phase-09-production-feature-implementation.md)
- [Phase 10: Commercial and Deployment Slice](docs/phase-10-commercial-deployment-slice.md)
- [Phase 11: Operations, Security, Analytics, and Deployment Hardening](docs/phase-11-operations-security-analytics.md)
- [Phase 12: Commercial UI, Mobile Integration, and Auth Recovery](docs/phase-12-commercial-ui-mobile-security.md)
- [Phase 13: External Readiness Validation](docs/phase-13-external-readiness-validation.md)
- [Phase 14: Deployment Readiness Completion](docs/phase-14-deployment-readiness-completion.md)
