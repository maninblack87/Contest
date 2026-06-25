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
    db.connect()

    def clear_entries():
        ent_id.delete(0, tk.END)
        ent_pw.delete(0, tk.END)
        ent_id.focus()

    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()
    db_id = result1[0]
    db_name = result1[1]
    db_role = result1[2]
    db_pw = result1[3]

    # 로그인 검증
    if id != db_id:
        messagebox.showerror("로그인 실패", "사번이 올바르지 않습니다")
        clear_entries()
        return
    
    if pw != db_pw:
        messagebox.showerror("로그인 실패", "암호가 올바르지 않습니다")
        clear_entries()
        return
    
    # 로그인 처리
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

    # 로그아웃 처리
    current_user = {
        "id" : "",
        "name" : "",
        "role" : "",
        "password" : ""
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    # 창 전환(w1)
    router.route_w1(root)


def change_password(ent_cur_pw:tk.Entry, ent_new_pw:tk.Entry, ent_conf_pw:tk.Entry, root:tk.Tk):
    cur_pw = ent_cur_pw.get()
    new_pw = ent_new_pw.get()
    conf_pw = ent_conf_pw.get()

    db = DBconn(DB_FILE)
    db.connect()
    
    # 현재 사용자 인증
    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)
    if cur_pw != current_user["password"]:
        messagebox.showerror("현재 사용자 인증 실패", "현재 사용자의 암호와 입력한 암호가 일치하지 않습니다")
        ent_cur_pw.delete(0, tk.END)
        ent_new_pw.delete(0, tk.END)
        ent_conf_pw.delete(0, tk.END)
        return
    
    # 조건 검증
    query1 = "select 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (current_user['id'],))
    result1 = db.cursor.fetchone()
    db_cur_pw = result1[0]

    if cur_pw != db_cur_pw:
        messagebox.showerror("암호 입력 오류", "현재 암호와 데이터베이스 암호 입력값이 서로 달라야 함")
        return
    if cur_pw == new_pw:
        messagebox.showerror("암호 입력 오류", "현재 암호와 새 암호 입력값이 서로 달라야 함")
        return
    if new_pw != conf_pw:
        messagebox.showerror("암호 입력 오류", "새 암호와 새 암호 확인 입력값이 서로 같아야 함")
        return
    
    # 암호 변경 처리
    update_query = "update 업무사용자 set 암호 = ? where 사번 = ?"
    db.cursor.execute(update_query, (cur_pw, current_user["id"],))
    db.conn.commit()

    # 현재 사용자 초기화
    current_user = {
        "id" : "",
        "name" : "",
        "role" : "",
        "password" : ""
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    # 로그인 화면으로 이동
    messagebox.showinfo("암호저장 완료", "암호 저장 완료")
    router.route_w1(root)