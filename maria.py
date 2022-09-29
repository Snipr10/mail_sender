# Module Imports
# import mariadb
import sys
import mariadb

import json
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER_DB", "parser")
PASSWORD = os.getenv("PASSWORD_DB", "9ExtUS8uRyF9FSDf")
HOST = os.getenv("HOST_DB", "192.168.5.11")
PORT = int(os.getenv("PORT_DB", 3306))
DATABASE = os.getenv("DATABASE_DB", "parser")


def get_cursor():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database=DATABASE
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    return cur, conn
