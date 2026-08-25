-- ============================================
-- Live Crypto Data Pipeline
-- Analytical SQL Queries
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