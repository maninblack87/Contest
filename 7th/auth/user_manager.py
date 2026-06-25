from DB.DBconn import DBconn
from config import DB_FILE, CURRENT_USER
from routes import router

import tkinter as tk
from tkinter import messagebox, ttk
import json

def login(ent_id:tk.Entry, ent_pw:tk.Entry, root:tk.Tk):
    id = ent_id.get()
    pw = ent_pw.get()

    def clear_entries():
        ent_id.delete(0, tk.END)
        ent_pw.delete(0, tk.END)

    print("로그인 시작")

    db = DBconn(DB_FILE)
    db.connect()

    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()

    if not result1:
        messagebox.showerror("로그인 실패", "존재하지 않는 아이디")
        clear_entries()
        return

    db_pw = result1[3]
    if pw != db_pw:
        messagebox.showerror("로그인 실패", "올바르지 않은 비밀번호")
        clear_entries()
        return
    
    # 로그인 처리
    current_user = {
        "id" : result1[0],
        "name" : result1[1],
        "role" : result1[2],
        "password" : result1[3]
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)
    print("로그인 처리가 성공적으로 완료")

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
    print("로그아웃 처리 성공")

    router.route_w1(root)


def change_password(ent_currpw:tk.Entry, ent_newpw:tk.Entry, ent_confpw:tk.Entry, root:tk.Tk):
    currpw = ent_currpw.get()
    newpw = ent_newpw.get()
    confpw = ent_confpw.get()

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if currpw != current_user["password"]:
        messagebox.showerror("현재 사용자 인증 실패", "현재 사용자 인증 실패")
        ent_currpw.delete(0, tk.END)
        ent_newpw.delete(0, tk.END)
        ent_confpw.delete(0, tk.END)
        return
    
    query1 = "select 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (current_user["id"],))
    result1 = db.cursor.fetchone()
    db_pw = result1[0]
    if currpw != db_pw:
        messagebox.showerror("암호저장 실패", "데이터베이스에 저장된 암호와 일치하지 않습니다")
        return
    if currpw == newpw:
        messagebox.showerror("암호저장 실패", "새로 저장될 암호는 현재 암호와 달라야 합니다")
        return
    if newpw != confpw:
        messagebox.showerror("암호저장 실패", "새로 저장될 암호와 새 암호 확인의 입력값이 같아야 합니다")
        return
    
    try:
        # 변경된 암호 저장
        update_query = "update 업무사용자 set 암호 = ? where 사번 = ?"
        db.cursor.execute(update_query, (newpw, current_user["id"],))
        db.conn.commit()

        messagebox.showinfo("암호저장 완료", "암호 저장 완료")
        router.route_w1(root)

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.close()