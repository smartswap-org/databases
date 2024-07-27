from loguru import logger

def create_db_smartswap(cursor):
    logger.info("Setting up the smartswap database.")
    cursor.execute("USE smartswap;")
    
    # Create tables if they do not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        name VARCHAR(50),
        address VARCHAR(255),
        private_key VARCHAR(255),
        PRIMARY KEY (name(50)) -- Using a prefix length for the index
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        user CHAR(100) PRIMARY KEY,
        discord_user_id VARCHAR(125),
        password VARCHAR(32)
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
    
    logger.info("Smartswap database setup completed.")