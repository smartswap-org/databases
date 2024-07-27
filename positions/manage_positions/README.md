### manage_positions

A brief overview of the functions used to manage the `smartswap_positions` database, which tracks trading positions on both centralized exchanges (CEX) and decentralized exchanges (DEX).

1. **`position_management.py`**
   - **`create_position(cursor, wallet_name, position_type)`**
     - Creates a new trading position.
     - Parameters: `cursor` (database cursor), `wallet_name` (str), `position_type` (str: 'CEX' or 'DEX').
     - Returns: `position_id` (int).

2. **`cex_market_management.py`**
   - **`cex_market_buy(cursor, position_id, buy_order_id, buy_price, buy_date, buy_quantity, buy_fees, exchange)`**
     - Inserts or updates purchase details for a CEX position.
     - Parameters: `cursor` (database cursor), `position_id` (int), `buy_order_id` (str), `buy_price` (float), `buy_date` (str), `buy_quantity` (float), `buy_fees` (float), `exchange` (str).
   
   - **`cex_market_sell(cursor, position_id, sell_order_id, sell_price, sell_date, sell_quantity, sell_fees)`**
     - Updates sale details for a CEX position.
     - Parameters: `cursor` (database cursor), `position_id` (int), `sell_order_id` (str), `sell_price` (float), `sell_date` (str), `sell_quantity` (float), `sell_fees` (float).

3. **`dex_router_management.py`**
   - **`dex_router_buy(cursor, position_id, buy_hash, buy_price, buy_date, buy_quantity, buy_fees)`**
     - Inserts or updates purchase details for a DEX position.
     - Parameters: `cursor` (database cursor), `position_id` (int), `buy_hash` (str), `buy_price` (float), `buy_date` (str), `buy_quantity` (float), `buy_fees` (float).

   - **`dex_router_sell(cursor, position_id, sell_hash, sell_price, sell_date, sell_quantity, sell_fees)`**
     - Updates sale details for a DEX position.
     - Parameters: `cursor` (database cursor), `position_id` (int), `sell_hash` (str), `sell_price` (float), `sell_date` (str), `sell_quantity` (float), `sell_fees` (float).
