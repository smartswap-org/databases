from logger import log
import pymysql
from create.user_manager import handle_user
from create.databases.smartswap import create_db_smartswap

def handle_databases(cursor):
    log.info("Starting database management.")
    cursor.execute("SHOW DATABASES;")
    existing_databases = [db['Database'] for db in cursor.fetchall()]
    databases_to_check = ['smartswap']
    
    log.info(f"Existing databases: {existing_databases}")
    
    if any(db in existing_databases for db in databases_to_check):
        response = input("One or more databases already exist. Do you want to drop and recreate them? (yes/no): ").strip().lower()
        if response == 'yes':
            for db in databases_to_check:
                if db in existing_databases:
                    log.info(f"Dropping database {db}...")
                    cursor.execute(f"DROP DATABASE {db};")
        else:
            log.info("Databases will not be dropped and recreated.")
            return 
     
    log.info("Creating databases...")
    for db in databases_to_check:
        cursor.execute(f"CREATE DATABASE {db};")
        log.info(f"Database {db} created.")


def create_databases(host, sql_user, sql_password, db_user, db_password):
    try:
        log.info(f"Connecting to the database host {host} as user {sql_user}.")
        connection = pymysql.connect(
            host=host,
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
                
                # Grant privileges to db_user
                log.info("Granting privileges to the user.")
                cursor.execute(f"GRANT ALL PRIVILEGES ON smartswap.* TO '{db_user}'@'localhost';")

                cursor.execute("FLUSH PRIVILEGES;")
                log.info("Privileges granted and flushed.")
                
                # Setup the smartswap database
                create_db_smartswap(cursor)
                connection.commit()
                
                log.info("SQL commands executed successfully.")
                
    except pymysql.MySQLError as e:
        log.error(f"Error: {e}")
    finally:
        log.info("Closing the connection.")
