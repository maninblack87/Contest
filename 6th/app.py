import os

from config import DB_FILE, DB_BUILDER
from db.DBconnection import DBconnection
import w1

def main():
    if not os.path.exists(DB_FILE):
        db = DBconnection(DB_FILE)
        db.connect()
        db.execute_sql(DB_BUILDER)
    
    w1.main()


if __name__ == "__main__":
    main()