# app.py
import os

from config import DB_FILE
from db.db_connection import db_connection
import w1

def main():
    """
    DB_FILE = db_file.sqlite
    """

    if not os.path.exists(DB_FILE):

        db = db_connection(DB_FILE)
        db.connect()
        db.execute_sql("db/db_set.sql")
        db.close()

    w1.main()


if __name__ == "__main__":
    main()