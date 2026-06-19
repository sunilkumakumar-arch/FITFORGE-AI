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
  if [[ "${SIMULATE_EXTERNAL_VALIDATION:-false}" == "true" ]]; then
    mkdir -p reports/validation
    test -f infrastructure/aws/terraform/main.tf
    test -f infrastructure/aws/terraform/modules/network/main.tf
    test -f infrastructure/aws/terraform/modules/data/main.tf
    test -f infrastructure/aws/terraform/modules/ecs/main.tf
    test -f infrastructure/aws/terraform/modules/monitoring/main.tf
    test -f infrastructure/aws/terraform/modules/schedules/main.tf
    cat > reports/validation/terraform-validation.json <<'JSON'
{"mode":"simulation","status":"passed","checks":["root terraform module present","network module present","data module present","ecs module present","monitoring module present","schedules module present"],"note":"Terraform CLI is unavailable; rerun without simulation with Terraform installed for fmt/init/validate."}
JSON
    echo "Terraform validation simulation passed. See reports/validation/terraform-validation.json"
  else
  echo "Terraform is not installed; skipping terraform validation."
  fi
fi
if command -v docker >/dev/null 2>&1; then
  docker compose -f docker-compose.local.yml config >/dev/null
else
  if [[ "${SIMULATE_EXTERNAL_VALIDATION:-false}" == "true" ]]; then
    test -f docker-compose.local.yml
    test -f services/api/Dockerfile
    test -f apps/admin-web/Dockerfile
    cat > reports/validation/docker-validation.json <<'JSON'
{"mode":"simulation","status":"passed","checks":["docker-compose.local.yml present","API Dockerfile present","admin web Dockerfile present"],"note":"Docker CLI is unavailable; rerun without simulation with Docker installed for compose config/build validation."}
JSON
    echo "Docker validation simulation passed. See reports/validation/docker-validation.json"
  else
  echo "Docker is not installed; skipping docker compose config validation."
  fi
fi
