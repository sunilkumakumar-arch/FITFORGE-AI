#!/usr/bin/env bash
set -euo pipefail
: "${DB_INSTANCE_IDENTIFIER:?DB_INSTANCE_IDENTIFIER is required}"
SNAPSHOT_ID="${DB_INSTANCE_IDENTIFIER}-manual-$(date -u +%Y%m%d%H%M%S)"
aws rds create-db-snapshot --db-instance-identifier "$DB_INSTANCE_IDENTIFIER" --db-snapshot-identifier "$SNAPSHOT_ID"
echo "Created snapshot $SNAPSHOT_ID"
