# app.py
import os

from db.dbconnection import DBconnection
from config import DB_FILE, SQL_FILE
import w1

def main():

    if not os.path.exists(DB_FILE):
        db = DBconnection(DB_FILE)
        db.connect()
        db.executesql(SQL_FILE)
    else:
        print(f"{DB_FILE}에 파일(혹은 경로)이 있는거로 되어있음.")

    w1.main()

if __name__ == "__main__":
    main()