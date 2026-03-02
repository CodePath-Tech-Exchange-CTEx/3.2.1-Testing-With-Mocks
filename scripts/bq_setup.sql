-- Example BigQuery setup for the "expenses" table.
--
-- This script creates a simple table and inserts three sample rows used
-- throughout the lesson. It represents the "Database dependency" from
-- Slide 10 in a minimal, concrete form.
--
-- The placeholder __TABLE_ID__ is replaced by the seed_bq.sh script with
-- a concrete value like:
--   alfredo-pomales-li.321_dataset.slides_example

CREATE TABLE IF NOT EXISTS `__TABLE_ID__` (
  vendor STRING,
  amount FLOAT64,
  currency STRING
);

INSERT INTO `__TABLE_ID__` (vendor, amount, currency)
VALUES
  ("Buckingham Palace", 15.45, "GBP"),
  ("Ghibli Museum", 4433.78, "JPY"),
  ("Frida Kahlo Museum", 602.67, "MXN");

