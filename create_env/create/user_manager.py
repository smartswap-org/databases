from logger import log

def handle_user(cursor, db_user, db_password):
    log.info("Starting user management.")
    cursor.execute("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = %s) AS user_exists", (db_user,))
    user_exists = cursor.fetchone()['user_exists']
    
    log.info(f"User exists check: {user_exists}")
    
    if user_exists:
        response = input(f"The user '{db_user}' already exists. Do you want to drop and recreate the user? (yes/no): ").strip().lower()
        if response == 'yes':
            log.info(f"Dropping user {db_user}...")
            cursor.execute(f"DROP USER '{db_user}'@'localhost';")
        else:
            log.info("User will not be dropped and recreated.")
            return 
    log.info(f"Creating user {db_user}.")
    cursor.execute(f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';")
    log.info(f"User {db_user} created.")
