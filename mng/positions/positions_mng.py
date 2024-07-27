from loguru import logger

def create_position(cursor, wallet_name, position_type):
    """Create a new position with initial details."""
    logger.info(f"Creating new position for wallet_name '{wallet_name}' with type {position_type}.")
    cursor.execute("""
    INSERT INTO positions (wallet_name, position_type)
    VALUES (%s, %s);
    """, (wallet_name, position_type))
    position_id = cursor.lastrowid
    logger.info(f"Position created with position_id {position_id}.")
    return position_id
