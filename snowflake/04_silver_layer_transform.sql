-- silver layer - parsing for columns
-- Snowflake magic, we use FLATTEN function to separate JSON structure 
-- for a traditional sql table. Data transformation

CREATE OR REPLACE VIEW nbp_silver_rates AS
SELECT
    raw_json:table::STRING as table_type,
    raw_json:no::STRING as table_no,
    raw_json:effectiveDate::DATE as rate_date,
    f.value:currency::STRING as currency_code,
    f.value:mid::FLOAT as exchange_rate
FROM nbp_db.raw_data.nbp_raw_ingestion,
LATERAL FLATTEN(input => raw_json:rates) f;