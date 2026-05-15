-- Does the Snowflake see the new file in Azure?
LIST @nbp_azure_stage;

-- If so, get it to the table (remember about the database context and the scheme)
COPY INTO nbp_db.raw_data.nbp_raw_ingestion (raw_json, filename)
FROM (
    SELECT $1, metadata$filename 
    FROM @nbp_db.public.nbp_azure_stage 
)
FILE_FORMAT = (FORMAT_NAME = 'nbp_db.public.nbp_json_format');

-- Check the silver layer (view)
SELECT * FROM nbp_db.public.nbp_silver_rates;