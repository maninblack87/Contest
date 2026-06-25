import tkinter as tk
from tkinter import messagebox
import json

from config import CURRENT_USER, DB_FILE
from db.DBconnection import DBconnection
from routes import router

def login(ent_id:tk.Entry, ent_pw:tk.Entry, root:tk.Tk):
    id = ent_id.get()
    pw = ent_pw.get()
    
    db = DBconnection(DB_FILE)
    db.connect()

    query1 = "select 사번, 이름, 권한, 암호 from 업무사용자 where 사번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()

    # 조건1
    if not result1:
        messagebox.showerror("로그인 실패", "존재하지 않는 사번입니다")
        return

    db_id = result1[0]
    db_name = result1[1]
    db_role = result1[2]
    db_pw = result1[3]

    # 조건2
    if pw != db_pw:
        messagebox.showerror("로그인 실패", "암호가 일치하지 않습니다")
        return

    # 모든 조건을 통과했다면, 현재 사용자 정보 저장/갱신
    current_user = {
        'id' : db_id,
        'name' : db_name,
        'role' : db_role,
        'password' : db_pw,
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)

    # 메인화면으로 이동
    router.route_w2(root)


def logout(root:tk.Tk):
    current_user = {
        'id' : '',
        'name' : '',
        'role' : '',
        'password' : '',
    }
    with open (CURRENT_USER, "w", encoding="utf-8") as f:
        json.dump(current_user, f, ensure_ascii=False, indent=4)
    
    router.route_w1(root)


def change_password(ent_curr_pw:tk.Entry, ent_new_pw:tk.Entry, ent_conf_pw:tk.Entry, root:tk.Tk):
    curr_pw = ent_curr_pw.get()
    new_pw = ent_new_pw.get()
    conf_pw = ent_conf_pw.get()

    # 내장 함수 : 입력창 초기화
    def clear_entries():
        ent_curr_pw.delete(0, tk.END)
        ent_new_pw.delete(0, tk.END)
        ent_conf_pw.delete(0, tk.END)

    db = DBconnection(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 현재 사용자 인증
    if curr_pw != current_user["password"]:
        messagebox.showerror("현재 사용자 인증 실패", "현재 사용자 인증 실패")
        clear_entries()
        return
    
    try:
    
        # 데이터베이스 사용자 인증
        query1 = "select 암호 from 업무사용자 where 사번 = ?"
        db.cursor.execute(query1, (current_user["id"],))
        result1 = db.cursor.fetchone()
        db_pw = result1[0]
        if curr_pw != db_pw:
            messagebox.showerror("데이터베이스 사용자 암호 인증 실패", "데이터베이스 사용자 암호 인증 실패")
            clear_entries()
            return
        
        # 현재 암호와 새 암호 비교
        if curr_pw == new_pw:
            messagebox.showerror("입력 오류", "입력한 새 암호는 현재 암호와 달라야 합니다")
            clear_entries()
            return
        
        # 새 암호와 새 암호 확인 비교
        if new_pw != conf_pw:
            messagebox.showerror("입력 오류", "새 암호 확인는 새 암호와 일치해야 합니다")
            clear_entries()
            return
        
        # 새 암호로 데이터베이스에 저장(갱신)
        update_query = "update 업무사용자 set 암호 = ? where 사번 = ?"
        db.cursor.execute(update_query, (new_pw, current_user["id"],))
        db.conn.commit()

        # 암호 저장 완료 메세지 후, 로그인 페이지로 이동
        messagebox.showinfo("암호 저장 완료", "암호 저장 완료")
        router.route_w1(root)
        

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    

    finally:
        db.close()