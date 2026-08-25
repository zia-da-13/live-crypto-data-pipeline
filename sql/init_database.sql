-- ============================================
-- Live Crypto Data Pipeline
-- PostgreSQL Database Setup
-- ============================================


-- ============================================
-- 1. Create Main Table
-- ============================================

CREATE TABLE IF NOT EXISTS crypto_market_data (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20),
    name VARCHAR(50),
    current_price NUMERIC,
    market_cap BIGINT,
    total_volume BIGINT,
    high_24h NUMERIC,
    low_24h NUMERIC,
    price_change_percentage_24h NUMERIC,
    last_updated TIMESTAMP,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- 2. Prevent Duplicate Snapshots
-- ============================================

CREATE UNIQUE INDEX IF NOT EXISTS
unique_coin_snapshot_index
ON crypto_market_data (
    coin_id,
    last_updated
);


-- ============================================
-- 3. Latest Crypto Prices View
-- ============================================

CREATE OR REPLACE VIEW latest_crypto_prices AS

SELECT DISTINCT ON (coin_id)
    coin_id,
    symbol,
    name,
    current_price,
    market_cap,
    total_volume,
    high_24h,
    low_24h,
    price_change_percentage_24h,
    last_updated,
    collected_at
FROM crypto_market_data
ORDER BY
    coin_id,
    collected_at DESC;


-- ============================================
-- 4. Crypto Price Summary View
-- ============================================

CREATE OR REPLACE VIEW crypto_price_summary AS

SELECT
    coin_id,
    ROUND(AVG(current_price), 2) AS average_price,
    MIN(current_price) AS lowest_price,
    MAX(current_price) AS highest_price,
    ROUND(AVG(total_volume), 2) AS average_volume,
    COUNT(*) AS total_records
FROM crypto_market_data
GROUP BY coin_id;


-- ============================================
-- 5. Useful Index
-- ============================================

CREATE INDEX IF NOT EXISTS
crypto_market_data_collected_at_index
ON crypto_market_data (
    collected_at
);


-- ============================================
-- Database Setup Complete
-- ============================================