import pymysql
from create.database_manager import handle_databases
from create.user_manager import handle_user
from create.databases.smartswap import create_db_smartswap
from loguru import logger 

def execute_sql_commands(host, sql_user, sql_password, db_user, db_password):
    try:
        logger.info(f"Connecting to the database host {host} as user {sql_user}.")
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
                logger.info("Granting privileges to the user.")
                cursor.execute(f"GRANT ALL PRIVILEGES ON smartswap.* TO '{db_user}'@'localhost';")
                cursor.execute("FLUSH PRIVILEGES;")
                logger.info("Privileges granted and flushed.")
                
                # Setup the smartswap database
                create_db_smartswap(cursor)
                connection.commit()
                
                logger.info("SQL commands executed successfully.")
                
    except pymysql.MySQLError as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Closing the connection.")
