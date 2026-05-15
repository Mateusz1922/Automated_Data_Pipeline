-- Time-Travel Show off

USE DATABASE nbp_db;
USE SCHEMA public;
-- Data check from 10 minutes ago
SELECT * FROM nbp_raw_ingestion AT(OFFSET => -600);

-- restore the table to the status before error, do not use when no error
-- CREATE OR REPLACE TABLE nbp_raw_ingestion_restored AS
-- SELECT * FROM nbp_raw_ingestion AT(OFFSET => -600);

-- Check which currency had the biggest increase in value last week
WITH currency_ranges AS (
    SELECT
        currency_code,
        currency_name,
        MIN(exchange_rate) as min_rate,
        MAX(exchange_rate) as max_rate
    FROM nbp_silver_rates
    -- Filtering the last week, based on a date
    WHERE rate_date >= DATEADD(day, -7, (SELECT MAX(rate_date) FROM nbp_silver_rates))
    GROUP BY currency_code, currency_name
)
SELECT 
    currency_code, 
    currency_name,
    min_rate, 
    max_rate,
    ROUND(((max_rate - min_rate) / min_rate) * 100, 2) as percent_change
FROM currency_ranges
ORDER BY percent_change DESC;

-- SELECT * FROM nbp_db.raw_data.nbp_raw_ingestion LIMIT 5;

-- TODO
-- -- Calculate the real gold value in the given currency
-- USE DATABASE nbp_db;
-- USE SCHEMA raw_data;

-- ----------------------------------------------------
-- -- 1. GOLD PRICES PREPARATION (silver for gold)
-- ----------------------------------------------------

-- -- we assume that the gold data land in the same table nbp_raw_ingestion
-- -- or in a similar one. We ingest it to a clean format

-- CREATE OR REPLACE VIEW nbp_db.public.nbp_silver_gold_prices AS
-- SELECT
--     raw_json:data::DATE as gold_date,
--     raw_json:cena::FLOAT as price_pln
-- FROM nbp_db.raw_data.nbp_raw_ingestion
-- WHERE raw_json:data IS NOT NULL; -- filter for the records with gold

-- SELECT * FROM nbp_db.raw_data.nbp_raw_ingestion WHERE raw_json:data IS NOT NULL LIMIT 5;
-- ----------------------------------------------------
-- -- 2. GOLD LAYER: Comparative analysis (GOLD VS USD/EUR)
-- ----------------------------------------------------
-- -- we calculate how many gold units we can buy for 100 units of the given currency
-- -- Formula: Value = (100 * Currency_Rate) / Gold_Price_PLN

-- CREATE OR REPLACE TABLE nbp_gold_currency_analysis AS
-- SELECT
--     s.rate_date,
--     s.currency_code,
--     s.exchange_rate as rate_to_pln,
--     g.price_pln as gold_price_pln,
--     -- how many grams of gold you can buy for 100 units of the currency (e.g. 100 USD)
--     ROUND((100 * s.exchange_rate) / g.price_pln, 4) as gold_grams_per_100_units,
--     -- gold price directly in the given currency
--     ROUND(g.price_pln / s.exchange_rate, 2) as gold_price_in_currency
-- FROM nbp_silver_rates s
-- JOIN nbp_silver_gold_prices g ON s.rate_date = g.gold_date
-- WHERE s.currency_code IN ('USD', 'EUR', 'CHF', 'GBP');

-- ----------------------------------------------------
-- -- 3. REPORT VIEW: (Agregation)
-- ----------------------------------------------------
-- -- acerage prices and time volatility
-- CREATE OR REPLACE VIEW nbp_gold_business_summary AS
-- SELECT
--     currency_code,
--     AVG(gold_price_in_currency) as avg_price,
--     MIN(gold_price_in_currency) as min_price,
--     MAX(gold_price_in_currency) as max_price,
--     STDDEV(gold_price_in_currency) as volatility
-- FROM nbp_gold_currency_analysis
-- GROUP BY currency_code;

-- -- show the results

-- -- 1. See the full analytical table (gold and currencies)
-- SELECT * FROM nbp_db.raw_data.nbp_gold_currency_analysis;

-- -- 2. See the full business summary (average prices, min, max, volatility)
-- SELECT * FROM nbp_db.raw_data.nbp_gold_business_summary;

-- SHOW VIEWS IN SCHEMA nbp_db.raw_data;

-- SELECT * FROM nbp_db.raw_data.nbp_silver_gold_prices;

-- SELECT * FROM nbp_db.raw_data.nbp_raw_ingestion LIMIT 5;
