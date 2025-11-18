# app.py
import tkinter as tk
from db.dbconn import DBconn

def main():

    # 데이터베이스를 초기화한다
    db = DBconn("db_file.sqlite")

    # 로그인 화면을 실행한다
    None


if __name__ == "__main__":
    main()