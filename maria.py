# Module Imports
import mariadb
import sys


def get_cursor():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="parser",
            password="9ExtUS8uRyF9FSDf",
            host="192.168.5.11",
            port=3306,
            database="parser"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    return cur
