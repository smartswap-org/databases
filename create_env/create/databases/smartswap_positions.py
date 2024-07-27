from loguru import logger

def create_db_smartswap_positions(cursor):
    logger.info("Setting up the smartswap_positions database.")
    cursor.execute("USE smartswap_positions;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        position_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        wallet_name VARCHAR(100),
        position_type ENUM('CEX', 'DEX')
    );
    """)
    
    # Table for storing market orders for centralized exchanges (CEX)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cex_market (
        position_id BIGINT,
        buy_order_id VARCHAR(50),
        buy_price DECIMAL(18, 8),
        buy_date TIMESTAMP,
        buy_quantity DECIMAL(18, 8),
        buy_fees DECIMAL(18, 8),
        sell_order_id VARCHAR(50),
        sell_price DECIMAL(18, 8),
        sell_date TIMESTAMP,
        sell_quantity DECIMAL(18, 8),
        sell_fees DECIMAL(18, 8),
        exchange VARCHAR(20),
        FOREIGN KEY (position_id) REFERENCES positions(position_id)
    );
    """)
    
    # Table for storing market orders for decentralized exchanges (DEX)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dex_routers (
        position_id BIGINT,
        buy_hash VARCHAR(66),
        buy_price DECIMAL(18, 8),
        buy_date TIMESTAMP,
        buy_quantity DECIMAL(18, 8),
        buy_fees DECIMAL(18, 8),
        sell_hash VARCHAR(66),
        sell_price DECIMAL(18, 8),
        sell_date TIMESTAMP,
        sell_quantity DECIMAL(18, 8),
        sell_fees DECIMAL(18, 8),
        router VARCHAR(50),
        FOREIGN KEY (position_id) REFERENCES positions(position_id)
    );
    """)
    
    logger.info("Smartswap_positions database setup completed.")
