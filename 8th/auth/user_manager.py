import tkinter as tk
from tkinter import messagebox
import json

from db.dbconn import DBconn
from config import DB_FILE, CURRENT_USER
from routes import router

def login(ent_id:tk.Entry, ent_pw:tk.Entry, root:tk.Tk):

    id = ent_id.get()
    pw = ent_pw.get()
    print("로그인 테스트 시작")

    db = DBconn(DB_FILE)
    db.connect()

    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()

    if not result1:
        messagebox.showerror("로그인 실패", "존재하지 않는 아이디입니다")
        return
    
    if pw != result1[3]:
        messagebox.showerror("로그인 실패", "암호가 일치하지 않습니다")
        return
    
    current_user = {
        "id" : result1[0],
        "name" : result1[1],
        "role" : result1[2],
        "password" : result1[3]
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    router.route_w2(root)

    print("로그인 테스트 종료")


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


def change_password(ent_current_pw:tk.Entry, ent_new_pw:tk.Entry, ent_confirm_pw:tk.Entry, root:tk.Tk):
    current_pw = ent_current_pw.get()
    new_pw = ent_new_pw.get()
    confirm_pw = ent_confirm_pw.get()

    def clear_entries():
        ent_current_pw.delete(0, tk.END)
        ent_new_pw.delete(0, tk.END)
        ent_confirm_pw.delete(0, tk.END)
        ent_current_pw.focus()

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_pw != current_user["password"]:
        messagebox.showerror("현재 사용자 인증 실패", "현재 사용자 암호가 일치하지 않습니다")
        clear_entries()
        return
    
    query1 = "select 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (current_user["id"],))
    result1 = db.cursor.fetchone()
    db_pw = result1[0]
    if current_pw != db_pw:
        messagebox.showerror("데이터베이스 인증 실패", "입력된 암호가 해당 데이터베이스의 암호와 일치하지 않습니다")
        clear_entries()
        return
    
    if current_pw == new_pw:
        messagebox.showerror("암호저장 실패", "입력이 올바르지 않습니다")
        clear_entries()
        return
    
    if new_pw != confirm_pw:
        messagebox.showerror("암호저장 실패", "입력이 올바르지 않습니다")
        clear_entries()
        return
    
    try:
        update_query = "update 업무사용자 set 암호 = ? where 사번 = ?"
        db.cursor.execute(update_query, (new_pw, current_user["id"],))
        db.conn.commit()

        messagebox.showinfo("암호저장 완료", "암호가 성공적으로 저장되었습니다")

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