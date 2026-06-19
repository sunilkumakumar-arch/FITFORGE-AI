#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports/security
echo "Running npm production audit..."
if npm audit --omit=dev --json > reports/security/npm-audit.json; then
  echo "npm audit passed"
else
  echo "npm audit reported findings. See reports/security/npm-audit.json"
fi
if [[ -n "${ZAP_TARGET_URL:-}" ]]; then
  if command -v docker >/dev/null 2>&1; then
    docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "$ZAP_TARGET_URL" -J zap-report.json || true
    mv zap-report.json reports/security/zap-report.json 2>/dev/null || true
  else
    echo "Docker is required for OWASP ZAP scan."
    exit 2
  fi
else
  echo "Set ZAP_TARGET_URL to run OWASP ZAP baseline scan."
fi
