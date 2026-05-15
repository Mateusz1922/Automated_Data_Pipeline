-- create warehouse (computing engine)
CREATE OR REPLACE WAREHOUSE nbp_wh
WITH WAREHOUSE_SIZE = "XSMALL"
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- create database and scheme
CREATE DATABASE IF NOT EXISTS nbp_db;
CREATE SCHEMA IF NOT EXISTS nbp_db.raw_data;
CREATE SCHEMA IF NOT EXISTS nbp_db.public;

-- set the work context
USE WAREHOUSE nbp_wh;
USE DATABASE nbp_db;
USE SCHEMA public;

