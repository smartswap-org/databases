# This script demonstrates how to use wallet management functions to interact with the `smartswap` database.
# It specifically shows how to create, update, and delete a wallet using the functions defined above.

import pymysql
from wallets.wallet_mng import create_wallet, update_wallet_address, update_wallet_keys, delete_wallet

HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'smartswap'

def main():
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # create wallets
            create_wallet(cursor, 'wallet1', '0x1234567890abcdef', {'private_key': '123'})
            create_wallet(cursor, 'wallet2', '0xfedcba0987654321', {'api_key': '456', 'api_secret': '789'})
            
            # delete wallets
            delete_wallet(cursor, 'wallet1')
            delete_wallet(cursor, 'wallet2')
            
        connection.commit()
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
