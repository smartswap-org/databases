from loguru import logger

def dex_router_buy(cursor, position_id, buy_hash, buy_price, buy_date, buy_quantity, buy_fees):
    """Update the DEX router table with buy details for a given position_id."""
    logger.info(f"Updating DEX router buy details for position_id {position_id}.")
    cursor.execute("""
    INSERT INTO dex_routers (position_id, buy_hash, buy_price, buy_date, buy_quantity, buy_fees)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        buy_hash = VALUES(buy_hash),
        buy_price = VALUES(buy_price),
        buy_date = VALUES(buy_date),
        buy_quantity = VALUES(buy_quantity),
        buy_fees = VALUES(buy_fees);
    """, (position_id, buy_hash, buy_price, buy_date, buy_quantity, buy_fees))
    logger.info(f"DEX router buy details updated for position_id {position_id}.")

def dex_router_sell(cursor, position_id, sell_hash, sell_price, sell_date, sell_quantity, sell_fees):
    """Update the DEX router table with sell details for a given position_id."""
    logger.info(f"Updating DEX router sell details for position_id {position_id}.")
    cursor.execute("""
    UPDATE dex_routers
    SET sell_hash = %s,
        sell_price = %s,
        sell_date = %s,
        sell_quantity = %s,
        sell_fees = %s
    WHERE position_id = %s;
    """, (sell_hash, sell_price, sell_date, sell_quantity, sell_fees, position_id))
    logger.info(f"DEX router sell details updated for position_id {position_id}.")
