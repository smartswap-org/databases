from logger import log

def cex_market_buy(cursor, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdc, exchange, pair, buy_signals, bot_id, fund_slot, order_status='FILLED'):
    """Insert into the CEX market table with buy details and return the auto-incremented position_id."""
    log.info(f"Inserting CEX market buy details.")
    cursor.execute("""
    INSERT INTO cex_market (buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdc, buy_order_type, exchange, pair, buy_signals, bot_id, fund_slot, order_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        buy_order_id = VALUES(buy_order_id),
        buy_price = VALUES(buy_price),
        buy_date = VALUES(buy_date),
        buy_quantity = VALUES(buy_quantity),
        buy_fees = VALUES(buy_fees),
        buy_value_usdc = VALUES(buy_value_usdc),
        buy_order_type = VALUES(buy_order_type),
        exchange = VALUES(exchange),
        pair = VALUES(pair),
        buy_signals = VALUES(buy_signals),
        bot_id = VALUES(bot_id),
        fund_slot = VALUES(fund_slot),
        order_status = VALUES(order_status);
    """, (buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, buy_value_usdc, 'LIMIT', exchange, pair, buy_signals, bot_id, fund_slot, order_status))
    cursor.connection.commit()
    position_id = cursor.lastrowid
    log.info(f"CEX market buy details inserted with position_id {position_id}.")
    cursor.execute("""
        INSERT INTO app (position_id, buy_log, sell_log)
        VALUES (%s, %s, %s)
    """, (position_id, False, False))
    cursor.connection.commit()
    log.info(f"App buy_log and sell_log inserted for position_id {position_id}.")
    return position_id

def cex_market_sell(cursor, position_id, sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, sell_value_usdc, ratio, position_duration, sell_signals):
    """Update the CEX market table with sell details for a given position_id."""
    log.info(f"Updating CEX market sell details for position_id {position_id}.")
    cursor.execute("""
    UPDATE cex_market
    SET sell_order_id = %s,
        sell_price = %s,
        sell_date = %s,
        sell_quantity = %s,
        sell_fees = %s,
        sell_value_usdc = %s,
        sell_order_type = %s,
        ratio = %s,
        position_duration = %s,
        sell_signals = %s,
        order_status = 'COMPLETED'
    WHERE position_id = %s;
    """, (sell_order_id, sell_price, sell_date, sell_quantity, sell_fees, sell_value_usdc, 'LIMIT', ratio, position_duration, sell_signals, position_id))
    cursor.connection.commit()
    log.info(f"CEX market sell details updated for position_id {position_id}.")
