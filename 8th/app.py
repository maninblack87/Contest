from config import DB_FILE, DB_STRUCTURE
from db.dbconn import DBconn
import w1

import os

def main():
    
    if not os.path.exists(DB_FILE):
        db = DBconn(DB_FILE)
        db.connect()
        db.execute_sql(DB_STRUCTURE)
        db.close()
    
    w1.main()


if __name__ == "__main__":
    main()