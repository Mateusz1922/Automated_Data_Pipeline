-- Time-Travel Show off
-- Data check from 10 minutes ago
SELECT * FROM nbp_raw_ingestion AT(OFFSET => -600);

-- restore the table to the status before error
CREATE OR REPLACE TABLE nbp_raw_ingestion_restored AS
SELECT * FROM nbp_raw_ingestion AT(OFFSET => -600);

-- Check which currency had the biggest increase in value last week
SELECT 
    currency_code, 
    MIN(exchange_rate) as min_rate, 
    MAX(exchange_rate) as max_rate,
    ((max_rate - min_rate) / min_rate) * 100 as percent_change
FROM nbp_silver_rates
GROUP BY currency_code
ORDER BY percent_change DESC;