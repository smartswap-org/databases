from loguru import logger

def handle_databases(cursor):
    logger.info("Starting database management.")
    cursor.execute("SHOW DATABASES;")
    existing_databases = [db['Database'] for db in cursor.fetchall()]
    databases_to_check = ['smartswap', 'smartswap_positions', 'smartswap_data']
    
    logger.info(f"Existing databases: {existing_databases}")
    
    if any(db in existing_databases for db in databases_to_check):
        response = input("One or more databases already exist. Do you want to drop and recreate them? (yes/no): ").strip().lower()
        if response == 'yes':
            for db in databases_to_check:
                if db in existing_databases:
                    logger.info(f"Dropping database {db}...")
                    cursor.execute(f"DROP DATABASE {db};")
        else:
            logger.info("Databases will not be dropped and recreated.")
            return 
     
    logger.info("Creating databases...")
    for db in databases_to_check:
        cursor.execute(f"CREATE DATABASE {db};")
        logger.info(f"Database {db} created.")
