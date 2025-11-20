# app.py
import tkinter as tk

from db.dbconn import DBconn
from views import viewLogin

def main():

    # >> 앱을 처음 실행할 때 수행할 때 <<
    # 데이터베이스를 세팅
    db = DBconn("db_file.sqlite")
    db.connect()

    # 로그인 화면을 실행한다
    viewLogin.main()


if __name__ == "__main__":
    main()