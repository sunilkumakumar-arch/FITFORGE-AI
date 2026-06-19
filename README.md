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
