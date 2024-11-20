from loguru import logger

def create_db_smartswap(cursor):
    logger.info("Setting up the smartswap database.")
    cursor.execute("USE smartswap;")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        name VARCHAR(50),
        address VARCHAR(255),
        `keys` BLOB,
        PRIMARY KEY (name)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        user CHAR(100),
        discord_user_id VARCHAR(125),
        password BLOB,
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
        sell_order_id BIGINT,
        sell_price DECIMAL(18, 8),
        sell_date TIMESTAMP,
        sell_quantity DECIMAL(18, 8),
        sell_fees DECIMAL(18, 8),
        sell_value_usdt DECIMAL(18, 8),
        exchange VARCHAR(20),
        ratio DECIMAL(18, 8),
        position_duration INTEGER,
        pair VARCHAR(20),
        buy_signals TEXT,
        sell_signals TEXT,
        bot_name VARCHAR(20),
        fund_slot INTEGER
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
        bot_name TEXT,
        last_position_id INTEGER,
        funds TEXT
    )
    ''')

    logger.info("Smartswap database setup completed.")
