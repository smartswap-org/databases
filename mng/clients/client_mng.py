from logger import log
from clients.crypt_password import encrypt_password, decrypt_password

POWER_LEVELS = {
    'SYS.ADMIN': 5,
    'DEVELOPER': 4,
    'REVIEWER': 3,
    'VIP': 2,
    'CLIENT': 1,
    'VISITOR': 0
}

def create_client(cursor, user, discord_user_id, password, power=POWER_LEVELS['VISITOR']):
    """Create a new client in the clients table."""
    log.info(f"Creating new client with user '{user}'.")
    encrypted_password = encrypt_password(password)
    cursor.execute("""
    INSERT INTO clients (user, discord_user_id, password, power)
    VALUES (%s, %s, %s, %s);
    """, (user, discord_user_id, encrypted_password, power))
    log.info(f"Client created with user '{user}'.")

def update_client_password(cursor, user, new_password):
    """Update the password for a given client."""
    log.info(f"Updating password for client '{user}'.")
    encrypted_password = encrypt_password(new_password)
    cursor.execute("""
    UPDATE clients
    SET password = %s
    WHERE user = %s;
    """, (encrypted_password, user))
    log.info(f"Password updated for client '{user}'.")

def delete_client(cursor, user):
    """Delete a client from the clients table."""
    log.info(f"Deleting client with user '{user}'.")
    cursor.execute("""
    DELETE FROM clients
    WHERE user = %s;
    """, (user,))
    log.info(f"Client '{user}' deleted.")

def get_client_password(cursor, user):
    """Retrieve and decrypt the password for a given client."""
    log.info(f"Retrieving password for client '{user}'.")
    cursor.execute("""
    SELECT password
    FROM clients
    WHERE user = %s;
    """, (user,))
    result = cursor.fetchone()
    if result:
        encrypted_password = result['password']
        decrypted_password = decrypt_password(encrypted_password)
        log.info(f"Password retrieved for client '{user}'.")
        return decrypted_password
    else:
        log.warning(f"No client found with user '{user}'.")
        return None