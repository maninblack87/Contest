# app.py
import tkinter as tk

from db.dbconn import DBconn
from views import viewLogin

def main():

    # 데이터베이스를 초기화한다
    db = DBconn("db_file.sqlite")
    db.connect()

    # 로그인 화면을 실행한다
    viewLogin.main()


if __name__ == "__main__":
    main()