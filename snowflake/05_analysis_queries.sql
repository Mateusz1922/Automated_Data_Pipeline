-- Time-Travel Show off
-- Data check from 10 minutes ago
SELECT * FROM nbp_raw_ingestion AT(OFFSET => -600);

-- restore the table to the status before error
CREATE OR REPLACE TABLE nbp_raw_ingestion_restored AS
SELECT * FROM nbp_raw_ingestion AT(OFFSET => -600);