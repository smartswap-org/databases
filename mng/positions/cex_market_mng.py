from loguru import logger

def cex_market_buy(cursor, position_id, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, exchange):
    """Update the CEX market table with buy details for a given position_id."""
    logger.info(f"Updating CEX market buy details for position_id {position_id}.")
    cursor.execute("""
    INSERT INTO cex_market (position_id, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, exchange)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        buy_order_id = VALUES(buy_order_id),
        buy_price = VALUES(buy_price),
        buy_date = VALUES(buy_date),
        buy_quantity = VALUES(buy_quantity),
        buy_fees = VALUES(buy_fees),
        exchange = VALUES(exchange);
    """, (position_id, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, exchange))
    logger.info(f"CEX market buy details updated for position_id {position_id}.")

def cex_market_sell(cursor, position_id, sell_order_id, sell_price, sell_date, sell_quantity, sell_fees):
    """Update the CEX market table with sell details for a given position_id."""
    logger.info(f"Updating CEX market sell details for position_id {position_id}.")
    cursor.execute("""
    UPDATE cex_market
    SET sell_order_id = %s,
        sell_price = %s,
        sell_date = %s,
        sell_quantity = %s,
        sell_fees = %s
    WHERE position_id = %s;
    """, (sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, position_id))
    logger.info(f"CEX market sell details updated for position_id {position_id}.")
