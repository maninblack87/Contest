# auth/login.py
import tkinter as tk
from tkinter import messagebox

import json

from config import DB_FILE
from db.db_connection import db_connection
from routes.router import run_w2

def login(id_ent:tk.Entry, pw_ent:tk.Entry, root:tk.Tk):
    """
    """
    id = id_ent.get()
    pw = pw_ent.get()

    # 데이터베이스 연결
    db = db_connection(DB_FILE)
    db.connect()

    print("데이터베이스 연결")

    # 데이터베이스로부터 대조할 데이터를 가져오기
    query1 = "select * from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()

    print("데이터베이스로부터 대조할 데이터를 가져오기")

    # 데이터베이스에 사용자 유무 여부 확인
    if not result1:

        messagebox.showerror("로그인 실패", "존재하지 않는 사용자입니다.")

        id_ent.delete(0, tk.END)
        pw_ent.delete(0, tk.END)

        return
    
    print("데이터베이스에 사용자 유무 여부 확인")
    
    # 암호 대조하기
    if pw != result1[3]:

        messagebox.showerror("로그인 실패", "아이디가 일치하지 않습니다.")

        id_ent.delete(0, tk.END)
        pw_ent.delete(0, tk.END)

        return
    
    print("암호 대조하기")
    
    # 로그인 할 사용자 정보
    current_user = {
        "id" : result1[0],
        "name" : result1[1],
        "role" : result1[2],
        "password" : result1[3]
    }

    print("로그인 할 사용자 정보")

    # 로그인 할 사용자 정보를 json 파일에 저장
    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    print("로그인 할 사용자 정보를 json 파일에 저장")

    # 다른 화면으로 라우팅
    run_w2(root)

    print("다른 화면으로 라우팅까지.. login.py 테스트 성공!")
