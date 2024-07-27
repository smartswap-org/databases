from loguru import logger
from create.config import default_host
from create.database_manager import create_databases

def get_db_input():
    db_user = input("Enter the db_user: ")
    db_password = input(f"Enter the db_password for {db_user}: ")
    logger.info(f"Received db_user: {db_user}")
    return db_user, db_password

def get_sql_input():
    sql_host = input(f"Enter the Host IP Address (by default {default_host}): ")
    if not sql_host: 
        sql_host = default_host
        logger.info(f"Host selected by default: {sql_host}")
    sql_user = input("Enter the sql_user (with privileges usually root): ")
    sql_password = input(f"Enter the sql_password for user {sql_user}: ")
    logger.info(f"Received sql_user: {sql_user}")
    return sql_host, sql_user, sql_password

if __name__ == "__main__":
    sql_host, sql_user, sql_password = get_sql_input()
    db_user, db_password = get_db_input()

    create_databases(sql_host, sql_user, sql_password, db_user, db_password)
    logger.info(f"Final db_user: {db_user}, db_password: {db_password}")
