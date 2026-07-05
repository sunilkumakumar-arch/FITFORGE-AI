# AGENTS.md

## Cursor Cloud specific instructions

### Overview
FITFORGE-AI is an npm-workspaces monorepo:
- `services/api` — NestJS + Prisma REST API (PostgreSQL). Global prefix `api/v1`, Swagger at `/docs`, listens on `PORT` (default `3000`).
- `apps/admin-web` — Next.js 15 admin dashboard. Reads `NEXT_PUBLIC_API_BASE_URL` (default `http://localhost:3000/api/v1`).
- `apps/mobile` — Flutter app (not part of the web/API dev loop; requires the Flutter SDK).

Standard commands are in the root `package.json`/`README.md` and each workspace's `package.json`. CI steps live in `.github/workflows/ci.yml`.

### Environment setup notes (non-obvious)
- **Dependency drift from `latest` pins:** most deps are pinned to `"latest"`. Prisma was pinned to `^6.19.3` in `services/api/package.json` because Prisma 7 (the current `latest`) makes `new PrismaClient()` (used in `prisma/seed.ts` and `src/core/prisma.service.ts`) throw. Do not bump Prisma to 7 without also passing options to `PrismaClient`.
- **Datasource URL:** `prisma/schema.prisma`'s `datasource db` block uses `url = env("DATABASE_URL")`, so `DATABASE_URL` must be set for `prisma generate`/`migrate` and at runtime. The API loads it from `services/api/.env` via `ConfigModule` (`envFilePath: ['.env', '.env.example']`).
- **Env files:** copy `services/api/.env.example` → `services/api/.env` and `apps/admin-web/.env.example` → `apps/admin-web/.env.local`. These are gitignored and must be recreated per fresh VM (the update script handles this).
- **Database:** PostgreSQL must be running locally with a `fitforge`/`fitforge` role and `fitforge_ai` database (matches `.env.example`). Docker is not installed; Postgres is installed via apt. Start it with `sudo pg_ctlcluster 16 main start`. After the DB is up, apply schema + seed: `cd services/api && npx prisma migrate deploy && npx ts-node prisma/seed.ts`. Seed creates admin `admin@fitforge.ai` / `Fitforge@12345`.

### Running the services (dev)
- API: `cd services/api && npm run start:dev` (watch mode, port 3000).
  - **Gotcha:** if a prior `npm run api:build` ran, `nest start --watch` can emit nothing ("Found 0 errors" but no `dist/main.js`) because `deleteOutDir` wipes `dist` while the stale `tsconfig.build.tsbuildinfo` makes tsc think it's up to date. Fix: `rm -f services/api/tsconfig.build.tsbuildinfo && rm -rf services/api/dist`, then restart.
- Web: `cd apps/admin-web && npm run dev -- -p 3001` (use a non-3000 port so it doesn't collide with the API). Login page at `/login`.

### Testing / checks
- API tests: `npm run api:test`. Note `src/memberships/memberships.service.spec.ts` has a date-dependent assertion (hard-coded `2026-07-01` end date) that fails once the system clock is past that date — this is a pre-existing time bomb, unrelated to environment setup.
- Web has no lint script; the closest checks are `npm run web:typecheck` and `npm run web:build`.
