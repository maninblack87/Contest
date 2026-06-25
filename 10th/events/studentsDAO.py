import tkinter as tk
from tkinter import ttk, messagebox
import json

from config import DB_FILE, CURRENT_USER
from db.DBconn import DBconn

def onclick_add(
    tree:ttk.Treeview, 
    t_major:ttk.Combobox, 
    t_id:tk.Entry, 
    t_name:tk.Entry, 
    r_id:tk.Entry, 
    r_name:tk.Entry, 
    r_email:tk.Entry, 
    r_major:ttk.Combobox, 
    r_state:ttk.Combobox, 
    btn_del:tk.Button
):
    
    # 상단 입력창이 공란 상태 - 학과는 '전체학과'
    t_major.current(0)
    t_id.delete(0, tk.END)
    t_name.delete(0, tk.END)

    # 우측 상세정보가 공란+활성화 상태 - 학과는 '선택', 상태는 '재학'
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
    # >> 우측 상세정보가 공란이 되면, 좌측 목록에 선택된 노드도 취소되어야 한다
    tree.focus("")
    tree.selection_remove(tree.selection())
    btn_del.config(state="disabled")


def onclick_save(
    tree:ttk.Treeview, 
    r_id:tk.Entry, 
    r_name:tk.Entry, 
    r_email:tk.Entry, 
    r_major:ttk.Combobox, 
    r_state:ttk.Combobox
): 
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()

    db = DBconn(DB_FILE)
    db.connect()

    # 사전 작업(추가/수정 전)
    query3 = "select 학과코드 from 학과정보 where 명칭 = ?"
    db.cursor.execute(query3, (major,))
    result3 = db.cursor.fetchone()
    major_code = result3[0]

    # 공통 조건
    if len(id) != 5 and not id.isdigit():
        messagebox.showerror("비정상적인 값", "학번은 5자리 숫자")
        return
    if len(name) < 2:
        messagebox.showerror("비정상적인 값", "이름은 2글자 이상")
        return
    if len(email) < 8:
        messagebox.showerror("비정상적인 값", "이메일은 8글자 이상")
        return

    # 추가/수정 여부를 확인하려면 **선택된 노드의 여부**를 확인하면 된다
    node = tree.focus()
    if not node:
        # 추가
        # 추가 처리 조건
        query4 = "select * from 학생정보 where 학번 = ?"
        db.cursor.execute(query4, (id,))
        result4 = db.cursor.fetchone()
        if result4:
            messagebox.showerror("추가 실패", "존재하는 학번입니다")
            return

        db_majors = []
        query2 = "select 명칭 from 학과정보"
        db.cursor.execute(query2)
        result2 = db.cursor.fetchall()
        for r in result2:
            db_majors.append(r[0])
        if major not in db_majors:
            messagebox.showerror("비정상적인 값", "학과는 데이터베이스의 학과 목록 중 하나의 값")
            return
        
        if state != "재학":
            messagebox.showerror("비정상적인 값", "상태는 재학이어야 함")
            return
        
        # 추가 처리
        insert_query = "insert into 학생정보 (학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"
        db.cursor.execute(insert_query, (id, name, email, major_code, state,))
        db.conn.commit()

        # 우측 상세정보 공란
        r_id.config(state="normal")

    else:
        # 수정
        # 수정 처리 조건
        query1 = "select A.학번, A.이름, A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
        db.cursor.execute(query1, (id,))
        result1 = db.cursor.fetchone()
        if (id, name, email, major, state) == (result1[0], result1[1], result1[2], result1[3], result1[4]):
            messagebox.showerror("수정 오류", "수정된 값이 없습니다")
            return
        
        db_majors = []
        query2 = "select 명칭 from 학과정보"
        db.cursor.execute(query2)
        result2 = db.cursor.fetchall()
        for r in result2:
            db_majors.append(r[0])
        if major not in db_majors:
            messagebox.showerror("비정상적인 값", "학과는 데이터베이스의 학과 목록 중 하나의 값")
            return
        
        # 수정 처리
        update_query = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ? where 학번 = ?"
        db.cursor.execute(update_query, (email, major_code, state, id,))
        db.conn.commit()

    # 추가/수정 처리 후, 좌측 목록 갱신
    query5 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
    db.cursor.execute(query5)
    result5 = db.cursor.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for r in result5:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))


def onclick_delete(
    tree:ttk.Treeview, 
    r_id:tk.Entry, 
    r_name:tk.Entry, 
    r_email:tk.Entry, 
    r_major:ttk.Combobox, 
    r_state:ttk.Combobox, 
    btn_del:tk.Button
):
    id = r_id.get()

    db = DBconn(DB_FILE)
    db. connect()
    
    # 삭제 처리
    delete_query = "delete from 학생정보 where 학번 = ?"
    db.cursor.execute(delete_query, (id,))
    db.conn.commit()

    # 좌측 목록 갱신
    query1 = "select A.이름, A.학번, B.명칭, A.학과 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
    db.cursor.execute(query1)
    result1 = db.cursor.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for r in result1:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

    # 우측 상세정보 공란
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

    # 삭제 버튼 비활성화
    btn_del.config(state="disabled")