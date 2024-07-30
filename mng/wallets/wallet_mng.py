from wallets.crypt_keys import encrypt_keys, decrypt_keys
from loguru import logger

def create_wallet(cursor, name, address, keys):
    """Create a new wallet in the wallets table."""
    logger.info(f"Creating new wallet with name '{name}'.")
    encrypted_keys = encrypt_keys(keys)  # encrypt the keys dictionary
    cursor.execute("""
    INSERT INTO wallets (`name`, `address`, `keys`)
    VALUES (%s, %s, %s);
    """, (name, address, encrypted_keys))
    logger.info(f"Wallet created with name '{name}'.")

def update_wallet_address(cursor, name, new_address):
    """Update the address for a given wallet."""
    logger.info(f"Updating address for wallet '{name}'.")
    cursor.execute("""
    UPDATE wallets
    SET `address` = %s
    WHERE `name` = %s;
    """, (new_address, name))
    logger.info(f"Address updated for wallet '{name}'.")

def update_wallet_keys(cursor, name, new_keys):
    """Update the keys for a given wallet."""
    logger.info(f"Updating keys for wallet '{name}'.")
    encrypted_keys = encrypt_keys(new_keys)  # encrypt the new keys dictionary
    cursor.execute("""
    UPDATE wallets
    SET `keys` = %s
    WHERE `name` = %s;
    """, (encrypted_keys, name))
    logger.info(f"Keys updated for wallet '{name}'.")

def delete_wallet(cursor, name):
    """Delete a wallet from the wallets table."""
    logger.info(f"Deleting wallet with name '{name}'.")
    cursor.execute("""
    DELETE FROM wallets
    WHERE `name` = %s;
    """, (name,))
    logger.info(f"Wallet '{name}' deleted.")

def get_wallet_keys(cursor, name):
    """Retrieve and decrypt the keys for a given wallet."""
    logger.info(f"Retrieving keys for wallet '{name}'.")
    cursor.execute("""
    SELECT `keys`
    FROM wallets
    WHERE `name` = %s;
    """, (name,))
    result = cursor.fetchone()
    if result:
        encrypted_keys = result['keys']
        decrypted_keys = decrypt_keys(encrypted_keys)
        logger.info(f"Keys retrieved for wallet '{name}'.")
        return decrypted_keys
    else:
        logger.warning(f"No wallet found with name '{name}'.")
        return None
