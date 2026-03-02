#!/usr/bin/env bash
set -euo pipefail

# Seed BigQuery with the sample "expenses" data used in this lesson.
#
# This script simulates the "Database dependency" from Slide 10:
# - a real external system that our code talks to
# - used by the "integration-ish" tests when RUN_BQ_TESTS is enabled
#
# Requirements:
# - gcloud SDK and bq CLI installed and authenticated
# - Environment variables (example):
#     export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
#     export BIGQUERY_DATASET="321_dataset"
#     export BIGQUERY_TABLE="slides_example"

if [[ -z "${GOOGLE_CLOUD_PROJECT:-}" || -z "${BIGQUERY_DATASET:-}" || -z "${BIGQUERY_TABLE:-}" ]]; then
  echo "ERROR: GOOGLE_CLOUD_PROJECT, BIGQUERY_DATASET, and BIGQUERY_TABLE must be set."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Seeding BigQuery table: ${GOOGLE_CLOUD_PROJECT}.${BIGQUERY_DATASET}.${BIGQUERY_TABLE}"

BQ_TABLE_ID="${GOOGLE_CLOUD_PROJECT}.${BIGQUERY_DATASET}.${BIGQUERY_TABLE}"

# Option 2: build a single fully-qualified table ID in the shell and
# substitute it into the SQL before sending it to BigQuery. This keeps
# the .sql file generic while avoiding ${...} being interpreted literally
# by BigQuery.
sed "s|__TABLE_ID__|${BQ_TABLE_ID}|g" "${SCRIPT_DIR}/bq_setup.sql" | bq query \
  --project_id="${GOOGLE_CLOUD_PROJECT}" \
  --use_legacy_sql=false

echo "Done. Sample expenses table is ready for integration-ish tests."

