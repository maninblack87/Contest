# stdDAO.py
import tkinter as tk
from tkinter import ttk, messagebox
import json

from db.dbconnection import DBconnection
from config import DB_FILE


# 추가 버튼 클릭시
def onclick_add(t_major:ttk.Combobox, t_id:tk.Entry, t_name:tk.Entry, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):

    t_major.config(state="readonly")
    t_major.delete(0, tk.END)
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
    r_major.current(0)                  # 선택
    r_state.config(state="readonly")
    r_state.current(0)                  # 재학


# 함수 : 저장 버튼 클릭시
def onclick_save(treeview:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()

    # 데이터베이스가 필요없는 조건
    if len(id) != 5 and id.isdigit():
        messagebox.showerror("비정상적인 값", "학번은 5자리 숫자만 허용됨")
        return
    if len(name) < 2:
        messagebox.showerror("비정상적인 값", "이름은 2글자 이상이어야 함")
        return
    if len(email) < 8:
        messagebox.showerror("비정상적인 값", "이메일은 8글자 이상이어야 함")
        return

    db = DBconnection(DB_FILE)
    db.connect()

    try:
        # 쿼리 >>
        # 하나의 학생 조회
        query1 = "select 학번, 이름, 이메일, 학과, 상태 from 학생정보 where 학번 = ?"
        db.cursor.execute(query1, (id,))
        result1 = db.cursor.fetchone()

        # 모든 학과 조회
        majors1 = ["선택"]
        query2 = "select 명칭 from 학과정보"
        db.cursor.execute(query2)
        result2 = db.cursor.fetchall()
        for r in result2:
            majors1.append(r[0])

        # 트리뷰 조회
        query3 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query3)
        result3 = db.cursor.fetchall()

        # 데이터베이스가 필요한 조건(추가+수정)
        if major not in majors1:
            messagebox.showerror("비정상적인 값", "학과는 존재하는 데이터베이스의 학과 중에 있어야 함")
            return
        
        print("테스트1: ")
        print(f"{result1}")

        # 1. 새로 추가하는 경우
        if not result1:
            print("추가 작업 시작")
            # 데이터에비스가 필요한 조건(추가)
            if state != "재학":
                messagebox.showerror("비정상적인 값", "상태는 재학이어야 함")
                return
            
            # 추가 처리
            insert_query = "insert into 학생정보(학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"
            db.cursor.execute(insert_query, (id, name, email, major, state,))
            db.conn.commit()
            
        # 2. 수정하는 경우
        else:
            print("수정 작업 시작")
            # 수정 처리
            update_query = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ?"
            db.cursor.execute(update_query, (email, major, state,))
            db.conn.commit()

        # 트리뷰 반영
        for i in treeview.get_children():
            treeview.delete(i)
        for r in result3:
            treeview.insert("", "end", values=(r[0], r[1], r[2], r[3]))

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return

    finally:
        db.close()


# 함수 : 삭제 버튼 클릭 시
def onclick_delete(r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, treeview:ttk.Treeview, btn_del:tk.Button):
    id = r_id.get()

    db = DBconnection(DB_FILE)
    db.connect()

    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 쿼리
    # 트리뷰 조회
    query1 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()

    delete_query = "delete from 학생정보 where 학번 = ?"
    db.cursor.execute(delete_query, (id,))
    db.conn.commit()

    for i in treeview.get_children():
        treeview.delete(i)
    for r in result1:
        treeview.insert("", "end", (r[0], r[1], r[2], r[3]))

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
    r_major.config(state="readonly")
    r_state.config(state="normal")
    r_state.delete(0, tk.END)
    r_state.config(state="readonly")

    if current_user["role"] == "user":
        r_email.config(state="disabled")
        r_major.config(state="disabled")
        r_state.config(state="disabled")
        
    btn_del.config(state="disabled")