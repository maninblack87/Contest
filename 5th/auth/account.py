# account.py
import tkinter as tk
from tkinter import messagebox
import json

from db.dbconnection import DBconnection
from config import DB_FILE
from routes import router

def login(entid:tk.Entry, entpw:tk.Entry, root:tk.Tk):
    id = entid.get()
    pw = entpw.get()

    db = DBconnection(DB_FILE)
    db.connect()

    print("로그인 테스트1")

    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()
    db_id = result1[0]
    db_name = result1[1]
    db_role = result1[2]
    db_pw = result1[3]
    print(f"로그인 테스트2 : result1 = {result1}")
    
    # 조건1
    if not result1:
        messagebox.showerror("로그인 실패", "존재하지 않는 아이디입니다")
        return
    
    print("로그인 테스트3")
    
    # 조건2
    if pw != db_pw:
        messagebox.showerror("로그인 실패", "암호가 일치하지 않습니다")
        return
    
    print("로그인 테스트4")
    
    current_user = {
        "id" : db_id,
        "name" : db_name,
        "role" : db_role,
        "password" : db_pw
    }
    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    print("로그인 테스트5")

    router.route_w2(root)

    print("로그인 테스트6")


def logout(root:tk.Tk):
    
    current_user = {
        "id" : "",
        "name" : "",
        "role" : "",
        "password" : ""
    }
    with open("CurrentUser.json", "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    print("로그아웃 테스트1")

    router.route_w1(root)

    print("로그아웃 테스트2")