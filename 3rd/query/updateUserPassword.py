# query/updataUserPassword.py
from tkinter import messagebox

from sqlite.DBconnection import DBconnection
from config import DB_FILE
from routes import Router

def update_user_password(current_id:str, new_pw:str):

    # 데이터베이스 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 업무사용자 비밀번호 암호 변경 수행
    query = "update 업무사용자 set 암호 = ? where 사번 = ?"
    db.cursor.execute(query, (new_pw, current_id, ))
    db.conn.commit()

    # 데이터베이스 연결 종료
    db.close()