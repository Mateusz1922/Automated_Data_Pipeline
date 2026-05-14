-- create warehouse (computing engine)
CREATE OR REPLACE WAREHOUSE nbp_wh
WITH WAREHOUSE_SIZE = "XSMALL"
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- create database and scheme
CREATE DATABASE nbp_db;
CREATE SCHEMA nbp_db.raw_data;

-- set the work context
USE WAREHOUSE nbp_wh;
USE DATABASE nbp_db;
USE SCHEMA raw_data;

