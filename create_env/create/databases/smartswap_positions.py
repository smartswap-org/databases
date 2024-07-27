from loguru import logger

def create_db_smartswap_positions(cursor):
    logger.info("Setting up smartswap_positions database.")
    cursor.execute("USE smartswap_positions;")
    
    # Table for storing market orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_orders (
        order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        order_type VARCHAR(20),
        side VARCHAR(10),
        quantity DECIMAL(18, 8),
        price DECIMAL(18, 8),
        status VARCHAR(20),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (symbol) REFERENCES market_data(symbol)
    );
    """)
    
    # Table for storing current positions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        position_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        entry_price DECIMAL(18, 8),
        quantity DECIMAL(18, 8),
        position_type VARCHAR(20),
        status VARCHAR(20),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (symbol) REFERENCES market_data(symbol)
    );
    """)
    
    # Table for storing order history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_history (
        history_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        order_id BIGINT,
        symbol VARCHAR(20),
        order_type VARCHAR(20),
        side VARCHAR(10),
        quantity DECIMAL(18, 8),
        price DECIMAL(18, 8),
        status VARCHAR(20),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES market_orders(order_id)
    );
    """)
    
    # Table for storing market data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        symbol VARCHAR(20) PRIMARY KEY,
        last_price DECIMAL(18, 8),
        bid_price DECIMAL(18, 8),
        ask_price DECIMAL(18, 8),
        volume DECIMAL(18, 8),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    logger.info("Positions database setup completed.")