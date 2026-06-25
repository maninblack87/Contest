from db.DBconn import DBconn
from config import DB_FILE, SQL_FILE
import w1

def main():
    db = DBconn(DB_FILE)
    db.connect()
    db.execute_sql(SQL_FILE)

    w1.main()


if __name__ == "__main__":
    main()