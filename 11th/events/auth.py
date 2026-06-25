import tkinter as tk
from tkinter import messagebox
import json

from db.DBconn import DBconn
from config import DB_FILE, CURRENT_USER
from routes import router

def login(ent_id:tk.Entry, ent_pw:tk.Entry, root:tk.Tk):
    id = ent_id.get()
    pw = ent_pw.get()

    db = DBconn(DB_FILE)
    
    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()

    if not result1:
        messagebox.showerror("로그인 실패", "존재하지 않는 사번")
        ent_id.delete(0, tk.END)
        ent_pw.delete(0, tk.END)
        db.close()
        return

    db_id, db_name, db_role, db_pw = result1
    
    if pw == db_pw:
        current_user = {
            "id" : db_id,
            "name" : db_name,
            "role" : db_role,
            "pw" : db_pw
        }
        with open (CURRENT_USER, "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)

        router.route_w2(root)

    else:
        messagebox.showerror("로그인 실패", "일치하지 않는 암호")
        ent_id.delete(0, tk.END)
        ent_pw.delete(0, tk.END)
        db.close()
        return
    

def logout(root:tk.Tk):
    current_user = {
        "id": "",
        "name": "",
        "role": "",
        "password": ""
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, ensure_ascii=False, indent=4)

    router.route_w1(root)


def change_pw(ent_curr:tk.Entry, ent_new:tk.Entry, ent_conf:tk.Entry, root:tk.Tk):
    curr = ent_curr.get()
    new = ent_new.get()
    conf = ent_conf.get()

    def clear_entries():
        ent_curr.delete(0, tk.END)
        ent_new.delete(0, tk.END)
        ent_conf.delete(0, tk.END)

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    db = DBconn(DB_FILE)

    if curr != current_user["password"]:
        messagebox.showerror("현재 사용자 인증실패", "현재 사용자 인증실패")
        clear_entries()
        return
    
    query1 = "select 사번, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (current_user["id"],))
    result1 = db.cursor.fetchone()
    db_id, db_pw = result1

    if curr != db_pw:
        messagebox.showerror("DB 인증실패", "DB 인증실패")
        return
    if curr == new:
        messagebox.showerror("DB 인증실패", "DB 인증실패")
        return
    if new != conf:
        messagebox.showerror("DB 인증실패", "DB 인증실패")
        return
    
    update_query = "update 업무사용자 set 암호 = ? where 사번 = ?"
    db.cursor.execute(update_query, (new, current_user["id"],))
    db.conn.commit()

    messagebox.showinfo("암호저장 완료", "암호저장 완료")
    router.route_w1(root)