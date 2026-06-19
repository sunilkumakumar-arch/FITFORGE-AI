# FITFORGE AI - Deployment Guide

This guide describes how to deploy FITFORGE AI using:

- AWS
- PostgreSQL
- Docker
- Next.js
- Flutter
- Razorpay
- WhatsApp Business API

It includes local deployment, production infrastructure setup, environment variables, deployment commands, and validation steps.

---

## 1. Repository Structure

```text
.
|-- apps/
|   |-- admin-web/          # Next.js admin dashboard
|   `-- mobile/             # Flutter mobile app
|-- services/
|   `-- api/                # NestJS backend API
|-- infrastructure/
|   |-- aws/terraform/      # AWS Terraform scaffold
|   `-- monitoring/         # CloudWatch dashboard scaffold
|-- scripts/                # Validation, backup, security, smoke test scripts
|-- docker-compose.local.yml
|-- package.json
`-- PROJECT_STATUS.md
```

---

## 2. Prerequisites

### Required Locally

- Node.js 22+
- npm 10+
- PostgreSQL 17+ or Docker
- Git

### Required for Full Deployment

- Docker
- Terraform
- AWS CLI
- AWS account with deployment permissions
- Razorpay test/live account
- WhatsApp Business API account
- Flutter SDK
- Android Studio for Android builds
- Xcode on macOS for iOS builds

---

## 3. Environment Variables

### Backend API

Create:

```bash
cp services/api/.env.example services/api/.env
```

Backend variables:

```env
DATABASE_URL=postgresql://fitforge:fitforge@localhost:5432/fitforge_ai?schema=public
JWT_ACCESS_SECRET=replace-with-strong-secret
JWT_REFRESH_SECRET=replace-with-strong-secret
JWT_ACCESS_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=30d
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=replace-with-razorpay-secret
RAZORPAY_WEBHOOK_SECRET=replace-with-webhook-secret
WHATSAPP_API_URL=https://graph.facebook.com/v20.0
WHATSAPP_PHONE_NUMBER_ID=replace-with-phone-number-id
WHATSAPP_ACCESS_TOKEN=replace-with-whatsapp-token
RATE_LIMIT_PER_MINUTE=120
PORT=3000
```

Production notes:

- Store secrets in AWS Secrets Manager.
- Do not commit `.env`.
- Use separate Razorpay and WhatsApp credentials for staging and production.
- Use long random values for JWT secrets.

### Next.js Admin Web

Create:

```bash
cp apps/admin-web/.env.example apps/admin-web/.env.local
```

Variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api/v1
```

Production example:

```env
NEXT_PUBLIC_API_BASE_URL=https://api.fitforge.ai/api/v1
```

### Flutter Mobile

The current Flutter source uses the API client default:

```text
http://localhost:3000/api/v1
```

Before production release, configure the mobile API base URL per build flavor:

- Development
- Staging
- Production

Recommended production value:

```text
https://api.fitforge.ai/api/v1
```

---

## 4. Local Development Setup

Install dependencies:

```bash
npm install
```

Validate backend schema:

```bash
npm run api:prisma:validate
```

Build backend:

```bash
npm run api:build
```

Run backend tests:

```bash
npm run api:test
```

Build admin web:

```bash
npm run web:build
```

Typecheck admin web:

```bash
npm run web:typecheck
```

---

## 5. Local Docker Deployment

Start PostgreSQL, Redis, API, and admin web:

```bash
docker compose -f docker-compose.local.yml up --build
```

Local URLs:

```text
API:       http://localhost:3000/api/v1
Swagger:   http://localhost:3000/docs
Admin Web: http://localhost:3001
Postgres:  localhost:5432
Redis:     localhost:6379
```

Stop services:

```bash
docker compose -f docker-compose.local.yml down
```

Remove local database volume:

```bash
docker compose -f docker-compose.local.yml down -v
```

---

## 6. PostgreSQL and Prisma

Validate Prisma schema:

```bash
npm run api:prisma:validate
```

Generate Prisma client:

```bash
npm run prisma:generate --workspace services/api
```

Run migrations in production:

```bash
npm run prisma:migrate:deploy --workspace services/api
```

Seed demo data:

```bash
npm run prisma:seed --workspace services/api
```

Current migration file:

```text
services/api/prisma/migrations/20260618203000_phase10_commerce_trainer_posture/migration.sql
```

Production database requirements:

- RDS PostgreSQL Multi-AZ
- Encryption at rest enabled
- Automated backups enabled
- Point-in-time recovery enabled
- TLS enforced

---

## 7. Backend API Deployment

### Docker Build

```bash
docker build -t fitforge-api ./services/api
```

Run locally:

```bash
docker run --env-file services/api/.env -p 3000:3000 fitforge-api
```

### AWS Deployment Target

Recommended AWS services:

- ECS Fargate for API containers
- ECR for Docker images
- RDS PostgreSQL
- ElastiCache Redis
- Secrets Manager
- CloudWatch Logs
- Application Load Balancer
- WAF

Push image to ECR:

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com
docker tag fitforge-api <account-id>.dkr.ecr.ap-south-1.amazonaws.com/fitforge-ai/api:latest
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/fitforge-ai/api:latest
```

Run migrations before service rollout:

```bash
npm run prisma:migrate:deploy --workspace services/api
```

---

## 8. Next.js Admin Web Deployment

### Local Build

```bash
npm run web:typecheck
npm run web:build
```

### Docker Build

```bash
docker build -f apps/admin-web/Dockerfile -t fitforge-admin-web .
```

Run:

```bash
docker run -e NEXT_PUBLIC_API_BASE_URL=https://api.fitforge.ai/api/v1 -p 3001:3000 fitforge-admin-web
```

### AWS Deployment Target

Recommended options:

1. ECS Fargate container behind ALB
2. Amplify Hosting
3. S3/CloudFront only if converted to static export

For the current app, use ECS Fargate or another Node-capable runtime.

---

## 9. Flutter Mobile Deployment

### Validate Flutter Source

```bash
npm run mobile:validate
```

This runs:

```bash
cd apps/mobile
flutter pub get
flutter analyze
flutter test
flutter build apk --debug
```

On macOS, it also runs:

```bash
flutter build ios --no-codesign
```

### Android Release Build

```bash
cd apps/mobile
flutter build appbundle --release
```

Upload output to Google Play Console.

### iOS Release Build

Run on macOS:

```bash
cd apps/mobile
flutter build ios --release
```

Then archive and distribute through Xcode/App Store Connect.

### Mobile Production Configuration

Before release:

- Set production API base URL.
- Configure Android package name.
- Configure iOS bundle identifier.
- Configure app signing.
- Configure camera permissions.
- Configure Razorpay Flutter keys.
- Configure push notification certificates if added.

---

## 10. Razorpay Setup

### Required Razorpay Values

```env
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=xxx
RAZORPAY_WEBHOOK_SECRET=xxx
```

### Verify Sandbox Credentials

```bash
RAZORPAY_KEY_ID=rzp_test_xxx RAZORPAY_KEY_SECRET=xxx npm run payments:verify:razorpay
```

The verification script:

- Creates a Razorpay order.
- Fetches the created order.
- Fails if credentials or API behavior are invalid.

### Configure Razorpay Webhook

In Razorpay Dashboard:

```text
Webhook URL: https://api.fitforge.ai/api/v1/payments/razorpay/webhook
Secret:      same value as RAZORPAY_WEBHOOK_SECRET
Events:      payment.captured, payment.failed, refund.processed
```

Backend validates webhook signatures.

---

## 11. WhatsApp Business API Setup

### Required WhatsApp Values

```env
WHATSAPP_API_URL=https://graph.facebook.com/v20.0
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_ACCESS_TOKEN=your-access-token
```

### Configure Webhook

Provider callback URL:

```text
https://api.fitforge.ai/api/v1/whatsapp/webhook
```

Verification endpoint:

```text
GET /api/v1/whatsapp/webhook
```

### Send Template Message

API endpoint:

```text
POST /api/v1/whatsapp/send-template
```

Example payload:

```json
{
  "to": "919999999999",
  "template": "membership_renewal",
  "language": "en_US"
}
```

Production requirements:

- Approved WhatsApp templates
- User opt-in
- Opt-out handling
- Delivery status monitoring

---

## 12. AWS Infrastructure

Terraform scaffold:

```text
infrastructure/aws/terraform
```

Validate Terraform:

```bash
terraform -chdir=infrastructure/aws/terraform fmt -check -recursive
terraform -chdir=infrastructure/aws/terraform init -backend=false
terraform -chdir=infrastructure/aws/terraform validate
```

Current Terraform modules:

- Network
- Data
- ECS
- Monitoring
- Schedules

Production AWS resources:

- VPC
- Public/private subnets
- ECS cluster
- ECR repositories
- RDS PostgreSQL
- Secrets Manager
- CloudWatch logs
- CloudWatch alarms
- SNS alert topic
- EventBridge schedules

---

## 13. Monitoring and Alerting

CloudWatch dashboard scaffold:

```text
infrastructure/monitoring/cloudwatch-dashboard.json
```

Terraform monitoring module:

```text
infrastructure/aws/terraform/modules/monitoring
```

Included alarm scaffolds:

- API 5xx
- API high latency

EventBridge schedule scaffold:

```text
infrastructure/aws/terraform/modules/schedules
```

Scheduled jobs:

- Release expired inventory reservations
- Scan membership renewals
- Aggregate daily branch metrics

---

## 14. Backup and Disaster Recovery

Manual RDS snapshot script:

```bash
DB_INSTANCE_IDENTIFIER=fitforge-ai-production scripts/backup-rds-snapshot.sh
```

Production backup requirements:

- RDS automated backups
- PITR enabled
- Daily snapshots
- Cross-region copy for production
- Quarterly restore tests

---

## 15. Security and OWASP Validation

Run security checks:

```bash
npm run security:owasp
```

Run OWASP ZAP against staging:

```bash
ZAP_TARGET_URL=https://staging.fitforge.ai npm run security:owasp
```

Outputs:

```text
reports/security/npm-audit.json
reports/security/zap-report.json
```

Notes:

- Reports are ignored by Git.
- Current npm audit may report upstream transitive findings from framework packages.
- Do not apply forced fixes that downgrade major framework versions without review.

---

## 16. Deployment Validation

Run local deployment validation:

```bash
npm run deploy:validate
```

This validates:

- Prisma schema
- Backend build
- Backend tests
- Web typecheck
- Web build
- Terraform if installed
- Docker Compose config if Docker is installed

Run simulated readiness validation when external tools are unavailable:

```bash
npm run readiness:simulate
```

This simulates:

- Flutter validation
- Razorpay sandbox verification
- OWASP ZAP gating
- Terraform validation
- Docker deployment validation

Run production smoke test after deployment:

```bash
API_BASE_URL=https://api.fitforge.ai/api/v1 scripts/smoke-test-production.sh
```

---

## 17. Recommended Production Release Sequence

1. Provision AWS infrastructure.
2. Configure Secrets Manager values.
3. Build and push API Docker image.
4. Build and push admin web Docker image.
5. Run Prisma migrations.
6. Seed initial roles and admin user.
7. Deploy API service.
8. Deploy admin web service.
9. Configure Razorpay webhook.
10. Configure WhatsApp webhook.
11. Run `npm run deploy:validate`.
12. Run Razorpay sandbox verification.
13. Run OWASP ZAP against staging.
14. Run production smoke tests.
15. Validate CloudWatch alarms.
16. Validate backup snapshot.
17. Release mobile apps through Play Console and App Store Connect.

---

## 18. Quick Command Reference

```bash
npm install
npm run api:prisma:validate
npm run api:build
npm run api:test
npm run web:typecheck
npm run web:build
npm run deploy:validate
npm run readiness:simulate
npm run security:owasp
npm run mobile:validate
RAZORPAY_KEY_ID=rzp_test_xxx RAZORPAY_KEY_SECRET=xxx npm run payments:verify:razorpay
docker compose -f docker-compose.local.yml up --build
```
