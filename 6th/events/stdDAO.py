import tkinter as tk
from tkinter import ttk, messagebox
import json

from config import CURRENT_USER, DB_FILE
from db.DBconnection import DBconnection

def onclick_add_btn(tree:ttk.Treeview, t_major:ttk.Combobox, t_id:tk.Entry, t_name:tk.Entry, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] == "user":
        return
    
    tree.selection_remove(tree.selection())

    t_major.config(state="readonly")
    t_major.current(0)
    t_id.config(state="normal")
    t_id.delete(0, tk.END)
    t_name.config(state="normal")
    t_name.delete(0, tk.END)

    r_id.config(state="normal")
    r_id.delete(0, tk.END)
    r_name.config(state="normal")
    r_name.delete(0, tk.END)
    r_email.config(state="normal")
    r_email.delete(0, tk.END)
    r_major.config(state="readonly")
    r_major.current(0)
    r_state.config(state="readonly")
    r_state.current(0)


def onclick_save_btn(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] == "user":
        return
    
    # 데이터베이스가 필요없는 조건
    if len(id) != 5 or not id.isdigit():
        messagebox.showerror("비정상적인 값", "학번은 5자리 숫자만 허용")
        return
    if len(name) < 2:
        messagebox.showerror("비정상적인 값", "이름은 최소 2글자 이상")
        return
    if len(email) < 8:
        messagebox.showerror("비정상적인 값", "이메일은 최소 8글자 이상")
        return

    db = DBconnection(DB_FILE)
    db.connect()

    try:
        # 입력 값에 대한 학과코드 구하기
        query5 = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query5, (major,))
        result5 = db.cursor.fetchone()
        major_code = result5[0]
    
        # 공통
        db_majors = []
        query3 = "select 명칭 from 학과정보"
        db.cursor.execute(query3)
        result3 = db.cursor.fetchall()
        for r in result3:
            db_majors.append(r[0])
        if major not in db_majors:
            messagebox.showerror("비정상적인 값", "학과는 데이터베이스 학과 목록 중 하나이어야 함")
            return

        selection = tree.selection()
        # 수정
        if selection:
            query1 = "select A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
            db.cursor.execute(query1, (id,))
            result1 = db.cursor.fetchone()
            if email == result1[0] and major == result1[1] and state == result1[2]:
                messagebox.showerror("수정 오류", "수정할 사항이 없습니다")
                return
            # 수정처리
            query4 = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ? where 학번 = ?"
            db.cursor.execute(query4, (email, major_code, state, id,))
            db.conn.commit()
                
        # 추가
        else:
            query2 = "select * from 학생정보 where 학번 = ?"
            db.cursor.execute(query2, (id,))
            result2 = db.cursor.fetchone()
            if result2:
                messagebox.showerror("비정상적인 값", "기존 학번데이터와 중복 금지")
                return
            if state != "재학":
                messagebox.showerror("비정상적인 값", "추가시 상태는 재학이어야 함")
                return
            
            # 추가처리
            query6 = "insert into 학생정보 (학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"
            db.cursor.execute(query6, (id, name, email, major_code, state))
            db.conn.commit()

        query7 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query7)
        result7 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result7:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))
        
    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류: {e}")

    finally:
        db.close()

    
def onclick_del_btn(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, del_btn:tk.Button):
    id = r_id.get()

    db = DBconnection(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    try:
        delete_query = "delete from 학생정보 where 학번 = ?"
        db.cursor.execute(delete_query, (id,))
        db.conn.commit()

        r_id.config(state="normal")
        r_id.delete(0, tk.END)
        r_id.config(state="disabled")
        r_name.config(state="normal")
        r_name.delete(0, tk.END)
        r_name.config(state="disabled")
        r_email.config(state="normal")
        r_email.delete(0, tk.END)
        r_major.config(state="normal")
        r_major.delete(0, tk.END)
        r_state.config(state="normal")
        r_state.delete(0, tk.END)

        if current_user["role"] == "user":
            r_email.config(state="disabled")
            r_major.config(state="disabled")
            r_state.config(state="disabled")

        query8 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query8)
        result8 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result8:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))
            
        del_btn.config(state="disabled")
        

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")

    
    finally:
        db.close()