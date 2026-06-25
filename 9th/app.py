import os

from config import DB_FILE, SET_SQL
from db.DBconn import DBconn
import w1

def main():

    if not os.path.exists(DB_FILE):
        db = DBconn(DB_FILE)
        db.connect()
        db.execute_sql(SET_SQL)
        db.close()

    w1.main()


if __name__ == "__main__":
    main()