-- Insert a client
INSERT INTO clients (user, discord_user_id, power, email)
VALUES ('trader1', '123456789', 1, 'trader1@example.com');

-- Insert a wallet
INSERT INTO wallets (name, address, `keys`, type)
VALUES ('binance_main', '0x123...456', AES_ENCRYPT('api_key:secret', 'key'), 'exchange');

-- Give wallet access to the client
INSERT INTO wallets_access (client_user, wallet_name)
VALUES ('trader1', 'binance_main');

-- Insert bot configurations
INSERT INTO bots (
    client_user,
    wallet_name,
    bot_name,
    exchange_name,
    pairs,
    strategy,
    reinvest_gains,
    position_percent_invest,
    invest_capital,
    adjust_with_profits_if_loss,
    timeframe,
    simulation,
    status
) VALUES 
(
    'trader1',
    'binance_main',
    'btc_scalper',
    'Binance',
    '["BTCUSDT"]',
    'QTS_daily_MAXER',
    TRUE,
    50.00,
    10.00,
    TRUE,
    '1d',
    TRUE,
    TRUE
);

