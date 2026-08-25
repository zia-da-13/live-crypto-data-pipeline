-- ============================================
-- Live Crypto Data Pipeline
-- Analytics and Views
-- ============================================


-- 1. Latest 10 records
SELECT
    coin_id,
    symbol,
    current_price,
    market_cap,
    total_volume,
    collected_at
FROM crypto_market_data
ORDER BY collected_at DESC
LIMIT 10;


-- 2. Total records collected for each coin
SELECT
    coin_id,
    COUNT(*) AS total_records
FROM crypto_market_data
GROUP BY coin_id
ORDER BY coin_id;


-- 3. Average collected price
SELECT
    coin_id,
    ROUND(AVG(current_price), 2) AS average_price
FROM crypto_market_data
GROUP BY coin_id
ORDER BY coin_id;


-- 4. Highest and lowest collected prices
SELECT
    coin_id,
    MAX(current_price) AS highest_price,
    MIN(current_price) AS lowest_price
FROM crypto_market_data
GROUP BY coin_id
ORDER BY coin_id;


-- 5. Latest price for each cryptocurrency
SELECT DISTINCT ON (coin_id)
    coin_id,
    symbol,
    current_price,
    market_cap,
    total_volume,
    collected_at
FROM crypto_market_data
ORDER BY coin_id, collected_at DESC;


-- 6. View: latest crypto prices
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
    collected_at
FROM crypto_market_data
ORDER BY coin_id, collected_at DESC;


-- 7. View: crypto price summary
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