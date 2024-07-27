import pymysql
import coloredlogs, logging

default_host = '192.168.1.1'

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def get_db_input():
    db_user = input("Enter the db_user: ")
    db_password = input(f"Enter the db_password for {db_user}: ")
    return db_user, db_password

def get_sql_input():
    sql_host = input(f"Enter the Host IP Adress (by default {default_host}): ")
    if not sql_host: 
        sql_host = default_host
        print('Host selected by default:', sql_host)
    sql_user = input("Enter the sql_user (with privileges usually root): ")
    sql_password = input(f"Enter the sql_password for user {sql_user}: ")
    return sql_host, sql_user, sql_password

def handle_databases(cursor):
    cursor.execute("SHOW DATABASES;")
    existing_databases = [db['Database'] for db in cursor.fetchall()]
    databases_to_check = ['smartswap', 'smartswap_positions', 'smartswap_data']
    
    if any(db in existing_databases for db in databases_to_check):
        response = input("One or more databases already exist. Do you want to drop and recreate them? (yes/no): ").strip().lower()
        if response == 'yes':
            for db in databases_to_check:
                if db in existing_databases:
                    logger.info(f"Dropping database {db}...")
                    cursor.execute(f"DROP DATABASE {db};")
        else:
            return 
    logger.info("Creating databases...")
    cursor.execute("CREATE DATABASE smartswap;")
    cursor.execute("CREATE DATABASE smartswap_positions;")
    cursor.execute("CREATE DATABASE smartswap_data;")

def handle_user(cursor, db_user, db_password):
    logger.info("Creating user...")
    cursor.execute("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = %s) AS user_exists", (db_user,))
    user_exists = cursor.fetchone()['user_exists']
    
    if user_exists:
        response = input(f"The user '{db_user}' already exists. Do you want to drop and recreate the user? (yes/no): ").strip().lower()
        if response == 'yes':
            logger.info(f"Dropping user {db_user}...")
            cursor.execute(f"DROP USER '{db_user}'@'localhost';")
        else:
            return 
    cursor.execute(f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';")


def execute_sql_commands(host, sql_user, sql_password, db_user, db_password):
    try:
        connection = pymysql.connect(
            host='localhost',
            user=sql_user,
            password=sql_password,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection:
            with connection.cursor() as cursor:
                handle_databases(cursor)
                connection.commit()
                handle_user(cursor, db_user, db_password)
                connection.commit()
                
                # privileges for db_user
                logger.info("Granting privileges...")
                cursor.execute(f"GRANT ALL PRIVILEGES ON smartswap.* TO '{db_user}'@'localhost';")
                cursor.execute("FLUSH PRIVILEGES;")

                # smartswap database setup
                logger.info("Setting up smartswap database...")
                cursor.execute("USE smartswap;")
                cursor.execute("""
                CREATE TABLE wallets (
                    name VARCHAR(50),
                    address VARCHAR(255),
                    private_key VARCHAR(255),
                    PRIMARY KEY (name(50)) -- Using a prefix length for the index
                );
                """)
                cursor.execute("""
                CREATE TABLE clients (
                    user CHAR(100) PRIMARY KEY,
                    discord_user_id VARCHAR(125),
                    password VARCHAR(32)
                );
                """)
                cursor.execute("""
                CREATE TABLE wallets_access (
                    client_user CHAR(100),
                    wallet_name VARCHAR(50),
                    PRIMARY KEY (client_user, wallet_name),
                    FOREIGN KEY (client_user) REFERENCES clients(user),
                    FOREIGN KEY (wallet_name) REFERENCES wallets(name)
                );
                """)
                
                connection.commit()
                logger.info("SQL commands executed successfully.")

    except pymysql.MySQLError as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Closing the connection.")

if __name__ == "__main__":
    sql_host, sql_user, sql_password = get_sql_input()
    db_user, db_password = get_db_input()

    execute_sql_commands(sql_host, sql_user, sql_password, db_user, db_password)
    logger.info(f"db_user: {db_user}, db_password: {db_password}")