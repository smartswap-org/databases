import json
from loguru import logger

def create_wallet(cursor, name, address, keys):
    """Create a new wallet in the wallets table."""
    logger.info(f"Creating new wallet with name '{name}'.")
    keys_json = json.dumps(keys)  # convert the keys dictionary to a JSON string
    cursor.execute("""
    INSERT INTO wallets (`name`, `address`, `keys`)
    VALUES (%s, %s, %s);
    """, (name, address, keys_json))
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
    keys_json = json.dumps(new_keys)  # convert the keys dictionary to a JSON string
    cursor.execute("""
    UPDATE wallets
    SET `keys` = %s
    WHERE `name` = %s;
    """, (keys_json, name))
    logger.info(f"Keys updated for wallet '{name}'.")

def delete_wallet(cursor, name):
    """Delete a wallet from the wallets table."""
    logger.info(f"Deleting wallet with name '{name}'.")
    cursor.execute("""
    DELETE FROM wallets
    WHERE `name` = %s;
    """, (name,))
    logger.info(f"Wallet '{name}' deleted.")
