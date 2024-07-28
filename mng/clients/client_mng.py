from loguru import logger

def create_client(cursor, user, discord_user_id, password):
    """Create a new client in the clients table."""
    logger.info(f"Creating new client with user '{user}'.")
    cursor.execute("""
    INSERT INTO clients (user, discord_user_id, password)
    VALUES (%s, %s, %s);
    """, (user, discord_user_id, password))
    logger.info(f"Client created with user '{user}'.")

def update_client_password(cursor, user, new_password):
    """Update the password for a given client."""
    logger.info(f"Updating password for client '{user}'.")
    cursor.execute("""
    UPDATE clients
    SET password = %s
    WHERE user = %s;
    """, (new_password, user))
    logger.info(f"Password updated for client '{user}'.")

def delete_client(cursor, user):
    """Delete a client from the clients table."""
    logger.info(f"Deleting client with user '{user}'.")
    cursor.execute("""
    DELETE FROM clients
    WHERE user = %s;
    """, (user,))
    logger.info(f"Client '{user}' deleted.")
