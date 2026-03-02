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
# - Environment variables:
#     GOOGLE_CLOUD_PROJECT
#     BIGQUERY_DATASET
#     BIGQUERY_TABLE

if [[ -z "${GOOGLE_CLOUD_PROJECT:-}" || -z "${BIGQUERY_DATASET:-}" || -z "${BIGQUERY_TABLE:-}" ]]; then
  echo "ERROR: GOOGLE_CLOUD_PROJECT, BIGQUERY_DATASET, and BIGQUERY_TABLE must be set."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Seeding BigQuery table: ${GOOGLE_CLOUD_PROJECT}.${BIGQUERY_DATASET}.${BIGQUERY_TABLE}"

bq query \
  --project_id="${GOOGLE_CLOUD_PROJECT}" \
  --use_legacy_sql=false \
  < "${SCRIPT_DIR}/bq_setup.sql"

echo "Done. Sample expenses table is ready for integration-ish tests."

