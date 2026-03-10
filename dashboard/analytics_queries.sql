SELECT symbol, AVG(price) as avg_price
FROM stock_prices
GROUP BY symbol;

SELECT MAX(price) as highest_price
FROM stock_prices;

SELECT COUNT(*) as total_records
FROM stock_prices;