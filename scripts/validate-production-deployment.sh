#!/usr/bin/env bash
set -euo pipefail
npm run api:prisma:validate
npm run api:build
npm run api:test
npm run web:typecheck
npm run web:build
if command -v terraform >/dev/null 2>&1; then
  terraform -chdir=infrastructure/aws/terraform fmt -check -recursive
  terraform -chdir=infrastructure/aws/terraform init -backend=false
  terraform -chdir=infrastructure/aws/terraform validate
else
  echo "Terraform is not installed; skipping terraform validation."
fi
if command -v docker >/dev/null 2>&1; then
  docker compose -f docker-compose.local.yml config >/dev/null
else
  echo "Docker is not installed; skipping docker compose config validation."
fi
