# FITFORGE AI - Phase 12 Commercial UI, Mobile Integration, and Auth Recovery

Status: Implemented after Phase 11

This phase addresses the next highest-priority production gaps from `PROJECT_STATUS.md`.

---

## Implemented Features

### Personal Training Credit Ledger

Files:

- `services/api/src/pt/dto/pt.dto.ts`
- `services/api/src/pt/pt.controller.ts`
- `services/api/src/pt/pt.service.ts`
- `services/api/src/pt/pt.service.spec.ts`

Endpoints:

- `POST /api/v1/pt/packages`
- `GET /api/v1/pt/packages`
- `POST /api/v1/pt/purchase`
- `POST /api/v1/pt/consume-credit`
- `GET /api/v1/pt/balance`

Capabilities:

- Create PT packages.
- Activate PT credits only after paid payment verification.
- Track credits in an append-only ledger.
- Consume credits when sessions are completed.
- Query available member/trainer credit balance.

### Password Reset Security Flow

Files:

- `services/api/src/auth/auth.service.ts`
- `services/api/src/auth/auth.controller.ts`
- `services/api/src/auth/auth-password-reset.spec.ts`

Endpoints:

- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`

Capabilities:

- Unknown emails do not leak account existence.
- Reset tokens are stored only as SHA-256 hashes.
- Reset tokens expire after 15 minutes.
- Reset completion revokes active refresh sessions.
- Password reset actions are audit logged.

### Admin Dashboard Production Forms

Files:

- `apps/admin-web/src/components/action-forms.tsx`
- `apps/admin-web/src/app/(app)/qr-attendance/page.tsx`
- `apps/admin-web/src/app/(app)/payments/page.tsx`
- `apps/admin-web/src/app/(app)/whatsapp/page.tsx`
- `apps/admin-web/src/app/(app)/trainer-bookings/page.tsx`

Capabilities:

- Generate branch QR tokens.
- Create Razorpay payment orders.
- Send WhatsApp templates.
- Create trainer bookings.

### Flutter Concrete Feature Screens

Files:

- `apps/mobile/lib/src/screens/qr_attendance_screen.dart`
- `apps/mobile/lib/src/screens/razorpay_checkout_screen.dart`
- `apps/mobile/lib/src/screens/posture_capture_screen.dart`
- `apps/mobile/lib/src/app.dart`
- `apps/mobile/lib/src/screens/home_screen.dart`

Capabilities:

- QR check-in screen.
- Razorpay order creation screen.
- AI posture demo-frame analysis screen.
- Member/trainer home navigation to concrete screens.

---

## Database Additions

Added Prisma models:

- `PasswordResetToken`
- `PtPackage`
- `PtCreditLedger`

The migration SQL was refreshed:

- `services/api/prisma/migrations/20260618203000_phase10_commerce_trainer_posture/migration.sql`

---

## Validation

Run:

```bash
npm run api:prisma:validate
npm run api:build
npm run api:test
npm run web:typecheck
npm run web:build
```

Flutter validation still requires a Flutter-enabled environment.

---

## Remaining Gaps

Key remaining gaps after this phase:

- Real Flutter package integration for QR scanning and Razorpay checkout.
- MediaPipe/MoveNet real camera pipeline.
- MFA.
- Email/SMS provider integrations.
- Live provider verification for Razorpay and WhatsApp.
- Production AWS apply and smoke testing.
- OWASP penetration test.
