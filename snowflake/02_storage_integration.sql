-- way of connecting the clouds
-- we create an integration object instead of writing the Azure 
-- access keys directly in the code
CREATE OR REPLACE STORAGE INTEGRATION azure_nbp_int
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = 'AZURE'
    ENABLED = TRUE
    AZURE_TENANT_ID = '<YOUR_TENANT_ID>'
    STORAGE_ALLOWED_LOCATIONS = ('<YOUR_STORAGE_URL>');

DESC STORAGE INTEGRATION azure_nbp_int;
-- azure_consent_url

-- snowflake must know that file in Azure are JSONs
-- define file format
CREATE OR REPLACE FILE FORMAT nbp_json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE; -- NBP returns data in a table [], so it pops it

-- create STAGE (bridge to Azure)
CREATE OR REPLACE STAGE nbp_azure_stage
    STORAGE_INTEGRATION = azure_nbp_int
    URL = '<YOUR_STORAGE_URL>'
    FILE_FORMAT = nbp_json_format;

-- connection test
-- LIST @nbp_azure_stage;