-- Bronze Layer - Raw Data
-- we don't need to start from a table with 50 columns
-- we create one column of type VARIANT, which accommodates
-- the whole JSON. It's the Schema-on-Read approach
CREATE OR REPLACE TABLE nbp_raw_ingestion (
    raw_json VARIANT,
    ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    filename STRING
);

-- DATA LOADING (we can invoke it manually or via ADF)
USE DATABASE nbp_db;

COPY INTO nbp_raw_ingestion (raw_json, filename)
FROM (
    SELECT $1, metadata$filename
    FROM @nbp_db.public.nbp_azure_stage
)
FILE_FORMAT = (FORMAT_NAME = 'nbp_db.public.nbp_json_format');

-- 3. Sprawdźmy, czy dane tam są
SELECT * FROM nbp_raw_ingestion;

-- SHOW STAGES IN ACCOUNT;
