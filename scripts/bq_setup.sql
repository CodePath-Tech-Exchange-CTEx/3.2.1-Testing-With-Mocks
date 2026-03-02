-- Example BigQuery setup for the "expenses" table.
--
-- This script creates a simple table and inserts three sample rows used
-- throughout the lesson. It represents the "Database dependency" from
-- Slide 10 in a minimal, concrete form.

CREATE TABLE IF NOT EXISTS `${GOOGLE_CLOUD_PROJECT}.${BIGQUERY_DATASET}.${BIGQUERY_TABLE}` (
  vendor STRING,
  amount FLOAT64,
  currency STRING
);

INSERT INTO `${GOOGLE_CLOUD_PROJECT}.${BIGQUERY_DATASET}.${BIGQUERY_TABLE}` (vendor, amount, currency)
VALUES
  ("Buckingham Palace", 15.45, "GBP"),
  ("Ghibli Museum", 4433.78, "JPY"),
  ("Frida Kahlo Museum", 602.67, "MXN");

