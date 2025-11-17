# app.py
import os

from config import DB_FILE
from sqlite.DBconnection import DBconnection
import w1

def main():
    """
    DB_FILE = db_file.sqlite
    """

    if not os.path.exists(DB_FILE):

        # (초기: 초기 데이터베이스가 생성 되기전 시점) 데이터베이스 및 테이블 생성
        db = DBconnection(DB_FILE)
        db.execute_sql("sqlite/DBstructure.sql")
        db.close()

    # 로그인 창(w1.py) 실행
    w1.main()

if __name__ == "__main__":
    main()