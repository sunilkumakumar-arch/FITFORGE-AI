#!/usr/bin/env bash
set -euo pipefail
: "${API_BASE_URL:?API_BASE_URL is required, e.g. https://api.example.com/api/v1}"
probe() {
  local method="$1" path="$2" expected="$3"
  local status
  status=$(curl -sS -o /tmp/fitforge-smoke.out -w "%{http_code}" -X "$method" "$API_BASE_URL$path" -H 'content-type: application/json')
  if [[ "$status" != "$expected" ]]; then
    echo "Smoke test failed for $method $path expected $expected got $status"
    cat /tmp/fitforge-smoke.out
    exit 1
  fi
  echo "OK $method $path -> $status"
}
probe GET /membership-plans 401
probe GET /products 401
probe GET /analytics/dashboard 401
probe POST /auth/login 400
