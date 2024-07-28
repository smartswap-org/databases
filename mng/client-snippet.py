# This script demonstrates how to use client management functions to interact with the `smartswap` database.
# It specifically shows how to create, update, and delete a client using the functions defined above.

import pymysql
from clients.client_mng import create_client, update_client_password, delete_client

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
            create_client(cursor, 'client1', '', 'securepassword')
            delete_client(cursor, 'client1')
            
        connection.commit()
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
