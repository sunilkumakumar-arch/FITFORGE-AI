# FITFORGE-AI
AI-powered fitness ecosystem

## Phase 5 Applications

- `apps/admin-web` - Next.js 15 web dashboards for Super Admin, Branch, Fitness Manager, Trainer, and Reception roles.
- `apps/mobile` - Flutter source architecture for Member and Trainer mobile apps targeting Android and iOS.

## Web Dashboard Commands

```bash
npm install
npm run web:dev
npm run web:typecheck
npm run web:lint
npm run web:build
```

## Mobile Commands

Flutter is required locally:

```bash
cd apps/mobile
flutter create --platforms=android,ios .
flutter analyze
flutter test
```
