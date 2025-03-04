INSERT INTO clients (user, discord_user_id, password, power)
VALUES ('trader1', '123456789', AES_ENCRYPT('securepass123', 'key'), 1);

INSERT INTO wallets (name, address, `keys`)
VALUES 
('binance_main', '0x123...456', AES_ENCRYPT('api_key:secret', 'key')),
('metamask_1', '0x789...012', AES_ENCRYPT('private_key', 'key'));

INSERT INTO wallets_access (client_user, wallet_name)
VALUES 
('trader1', 'binance_main'),
('trader1', 'metamask_1');

INSERT INTO bots (
    client_user, wallet_name, bot_name, exchange_name, pairs,
    strategy, reinvest_gains, position_percent_invest, invest_capital,
    adjust_with_profits_if_loss, timeframe, simulation
)
VALUES 
(
    'trader1', 'binance_main', 'BTC_SCALPER', 'Binance',
    '["BTCUSDT"]', 'RSI_MACD', TRUE, 50.00, 1000.00,
    TRUE, '5m', FALSE
),
(
    'trader1', 'binance_main', 'ETH_SWING', 'Binance',
    '["ETHUSDT"]', 'EMA_VOL', TRUE, 75.00, 2000.00,
    TRUE, '1h', FALSE
);

SET @btc_bot_id = (SELECT bot_id FROM bots WHERE bot_name = 'BTC_SCALPER');
SET @eth_bot_id = (SELECT bot_id FROM bots WHERE bot_name = 'ETH_SWING');

INSERT INTO funds (bot_id, last_position_id, funds)
VALUES 
(@btc_bot_id, 0, '{"USDT": 1000.00, "BTC": 0.00}'),
(@eth_bot_id, 0, '{"USDT": 2000.00, "ETH": 0.00}');

INSERT INTO cex_market (
    buy_order_id, buy_price, buy_date, buy_quantity, buy_fees,
    buy_value_usdt, buy_order_type, exchange, pair, buy_signals,
    bot_id, fund_slot
) VALUES (
    123456789, 45000.00, NOW() - INTERVAL 2 HOUR, 0.02, 0.45,
    900.00, 'MARKET', 'Binance', 'BTCUSDT', 
    '{"RSI_14": 30, "MACD_CROSS": true, "EMA_50_200_CROSS": true}',
    @btc_bot_id, 1
);

SET @btc_position_id = LAST_INSERT_ID();

INSERT INTO app (position_id, buy_log, sell_log)
VALUES (@btc_position_id, TRUE, FALSE);

UPDATE funds 
SET last_position_id = @btc_position_id,
    funds = '{"USDT": 100.00, "BTC": 0.02}'
WHERE bot_id = @btc_bot_id;

INSERT INTO cex_market (
    buy_order_id, buy_price, buy_date, buy_quantity, buy_fees,
    buy_value_usdt, buy_order_type, exchange, pair, buy_signals,
    bot_id, fund_slot
) VALUES (
    987654321, 2500.00, NOW() - INTERVAL 1 DAY, 0.8, 0.20,
    2000.00, 'LIMIT', 'Binance', 'ETHUSDT', 
    '{"EMA_CROSS": true, "VOL_SPIKE": true, "SUPPORT_LEVEL": 2450}',
    @eth_bot_id, 1
);

SET @eth_position_id = LAST_INSERT_ID();

INSERT INTO app (position_id, buy_log, sell_log)
VALUES (@eth_position_id, TRUE, FALSE);

UPDATE funds 
SET last_position_id = @eth_position_id,
    funds = '{"USDT": 0.00, "ETH": 0.8}'
WHERE bot_id = @eth_bot_id;

UPDATE cex_market
SET 
    sell_order_id = 123456790,
    sell_price = 46000.00,
    sell_date = NOW(),
    sell_quantity = 0.02,
    sell_fees = 0.46,
    sell_value_usdt = 920.00,
    sell_order_type = 'MARKET',
    ratio = (920.00 - 900.00) / 900.00,
    position_duration = TIMESTAMPDIFF(SECOND, buy_date, sell_date),
    sell_signals = '{"TAKE_PROFIT": true, "RSI_14": 70, "PROFIT_TARGET": "2%"}'
WHERE position_id = @btc_position_id;

UPDATE funds 
SET funds = '{"USDT": 920.00, "BTC": 0.00}'
WHERE bot_id = @btc_bot_id;

UPDATE app
SET sell_log = TRUE
WHERE position_id = @btc_position_id;

INSERT INTO connection_logs (
    user, ip_address, user_agent, browser, browser_version,
    os, os_version, device_type, screen_resolution, language,
    timezone, is_mobile, is_tablet, is_bot
) VALUES (
    'trader1', '192.168.1.100',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Chrome', '120.0.0.0',
    'Windows', '10', 'desktop',
    '1920x1080', 'en-US',
    'UTC+1', FALSE, FALSE, FALSE
);