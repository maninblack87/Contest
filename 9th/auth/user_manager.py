import tkinter as tk
from tkinter import messagebox
import json

from config import DB_FILE, CURRENT_USER
from db.DBconn import DBconn
from routes import router

def login(ent_id:tk.Entry, ent_pw:tk.Entry, root:tk.Tk):
    id = ent_id.get()
    pw = ent_pw.get()

    def clear_entries():
        ent_id.delete(0, tk.END)
        ent_pw.delete(0, tk.END)
        ent_id.focus()

    db = DBconn(DB_FILE)
    db.connect()

    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()
    db_id = result1[0]
    db_name = result1[1]
    db_role = result1[2]
    db_pw = result1[3]

    if id != db_id:
        messagebox.showerror("로그인 실패", "사번이 올바르게 입력되어야 합니다")
        clear_entries()
        return
    
    if pw != db_pw:
        messagebox.showerror("로그인 실패", "암호가 올바르게 입력되어야 합니다")
        clear_entries()
        return
    
    current_user = {
        'id' : db_id,
        'name' : db_name,
        'role' : db_role,
        'password' : db_pw
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    router.route_w2(root)


def logout(root:tk.Tk):
    current_user = {
        "id" : "",
        "name" : "",
        "role" : "",
        "password" : ""
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)
    
    router.route_w1(root)


def change_password(ent_curr_pw:tk.Entry, ent_new_pw:tk.Entry, ent_conf_pw:tk.Entry, btn_save:tk.Button, root:tk.Tk):
    curr_pw = ent_curr_pw.get()
    new_pw = ent_new_pw.get()
    conf_pw = ent_conf_pw.get()

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if curr_pw != current_user["password"]:
        messagebox.showerror("현재 사용자 인증 실패", "현재 사용자 인증 실패")
        ent_curr_pw.delete(0, tk.END)
        ent_new_pw.delete(0, tk.END)
        ent_conf_pw.delete(0, tk.END)
        return
    
    query1 = "select 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (current_user["id"],))
    db_pw = db.cursor.fetchone()[0]
    if curr_pw != db_pw:
        messagebox.showerror("암호저장 실패", "데이터베이스의 암호와 일치하지 않습니다")
        return
    
    if curr_pw == new_pw:
        messagebox.showerror("암호저장 실패", "현재 암호가 새 암호와 달라야 함")
        return
    
    if new_pw != conf_pw:
        messagebox.showerror("암호저장 실패", "새 암호가 새 암호 확인과 달라야 함")
        return
    
    try:
        update_query = "update 업무사용자 set 암호 = ? where 사번 = ?"
        db.cursor.execute(update_query, (new_pw, current_user["id"]))
        db.conn.commit()

        messagebox.showinfo("암호저장 완료", "암호저장 완료")
        current_user = {
            "id" : "",
            "name" : "",
            "role" : "",
            "password" : ""
        }
        with open (CURRENT_USER, "w", encoding="utf-8") as f:
            json.dump(current_user, f, ensure_ascii=False, indent=4)
        router.route_w1(root)

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.close()