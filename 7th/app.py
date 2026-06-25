import os

from config import DB_FILE, DB_SET
from DB.DBconn import DBconn

import w1

def main():

    if not os.path.exists(DB_FILE):
        db = DBconn(DB_FILE)
        print("test _ DB연결 시작")
        db.connect()
        print("test _ DB연결 완료")
        db.execute_sql(DB_SET)
        print("test _ DB구성 완료")
        db.close()
        print("test _ DB연결 종료")

    w1.main()
    

if __name__ == "__main__":
    main()