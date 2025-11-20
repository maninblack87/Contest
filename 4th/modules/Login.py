# modules/Login.py
import json
import tkinter as tk
from tkinter import messagebox

from config import DB_FILE
from db.dbconn import DBconn
from routes import Router

def login(ipt_id:tk.Entry, ipt_pw:tk.Entry, master:tk.Widget):

    # 데이터베이스 연결
    db = DBconn(DB_FILE)
    db.connect()

    # 데이터베이스에서 입력한 사번과 비밀번호와 일치하는 사용자 정보를 조회
    query1 = """
        select 사번, 이름, 권한, 암호 
        from 업무사용자 
        where 사번 = ? and 암호 = ?
        """
    db.cursor.execute(query1, (ipt_id, ipt_pw,))
    result1 = db.cursor.fetchone()

    if result1:

        current_user = {
            "id" : result1[0],
            "name" : result1[1],
            "role" : result1[2],
            "password" : result1[3],
        }

        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

    else:

        messagebox.showerror("", "로그인 실패")

        ipt_id.delete(0, tk.END)
        ipt_pw.delete(0, tk.END)

        return
    
    # 메인 창으로 이동
    Router.run_main(master)