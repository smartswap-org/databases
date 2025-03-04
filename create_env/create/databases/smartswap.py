from loguru import logger

def create_db_smartswap(cursor):
    logger.info("Setting up the smartswap database.")
    cursor.execute("USE smartswap;")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        name VARCHAR(50),
        address VARCHAR(255),
        `keys` BLOB,
        type VARCHAR(20), 
        PRIMARY KEY (name)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        user CHAR(100),
        discord_user_id VARCHAR(125),
        password BLOB,
        power INTEGER DEFAULT 0,
        email VARCHAR(255) DEFAULT NULL,
        PRIMARY KEY (user)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets_access (
        client_user CHAR(100),
        wallet_name VARCHAR(50),
        PRIMARY KEY (client_user, wallet_name),
        FOREIGN KEY (client_user) REFERENCES clients(user),
        FOREIGN KEY (wallet_name) REFERENCES wallets(name)
    );
    """)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cex_market (
        position_id INTEGER PRIMARY KEY AUTO_INCREMENT,
        buy_order_id BIGINT,
        buy_price DECIMAL(18, 8),
        buy_date TIMESTAMP,
        buy_quantity DECIMAL(18, 8),
        buy_fees DECIMAL(18, 8),
        buy_value_usdt DECIMAL(18, 8),
        buy_order_type VARCHAR(20) DEFAULT NULL,
        sell_order_id BIGINT,
        sell_price DECIMAL(18, 8),
        sell_date TIMESTAMP,
        sell_quantity DECIMAL(18, 8),
        sell_fees DECIMAL(18, 8),
        sell_value_usdt DECIMAL(18, 8),
        sell_order_type VARCHAR(20) DEFAULT NULL,
        exchange VARCHAR(20),
        ratio DECIMAL(18, 8),
        position_duration INTEGER,
        pair VARCHAR(20),
        buy_signals TEXT,
        sell_signals TEXT,
        bot_id INTEGER,
        fund_slot INTEGER DEFAULT 0,
        FOREIGN KEY (bot_id) REFERENCES bots(bot_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS app (
        position_id INTEGER PRIMARY KEY,
        buy_log BOOLEAN DEFAULT FALSE,
        sell_log BOOLEAN DEFAULT FALSE
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funds (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        bot_id INTEGER,
        last_position_id INTEGER,
        funds TEXT,
        FOREIGN KEY (bot_id) REFERENCES bots(bot_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connection_logs (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        user CHAR(100),
        connection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(45),
        user_agent TEXT,
        browser VARCHAR(50),
        browser_version VARCHAR(30),
        os VARCHAR(50),
        os_version VARCHAR(30),
        device_type VARCHAR(20),
        screen_resolution VARCHAR(20),
        language VARCHAR(10),
        timezone VARCHAR(50),
        is_mobile BOOLEAN,
        is_tablet BOOLEAN,
        is_bot BOOLEAN,
        referrer TEXT,
        FOREIGN KEY (user) REFERENCES clients(user),
        INDEX idx_user_date (user, connection_date)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bots (
        bot_id INTEGER PRIMARY KEY AUTO_INCREMENT,
        client_user CHAR(100),
        wallet_name VARCHAR(50),
        bot_name VARCHAR(50),
        exchange_name VARCHAR(50),
        pairs TEXT,
        strategy VARCHAR(50),
        reinvest_gains BOOLEAN,
        position_percent_invest DECIMAL(5, 2),
        invest_capital DECIMAL(18, 2),
        adjust_with_profits_if_loss BOOLEAN,
        timeframe VARCHAR(10),
        simulation BOOLEAN,
        status BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (client_user) REFERENCES clients(user),
        FOREIGN KEY (wallet_name) REFERENCES wallets(name)
    );
    ''')

    logger.info("Smartswap database setup completed.")
