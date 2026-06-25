import tkinter as tk
from tkinter import ttk, messagebox
import json

from config import CURRENT_USER, DB_FILE
from db.DBconn import DBconn

def search(ent_major:ttk.Combobox, ent_id:tk.Entry, ent_name:tk.Entry, tree:ttk.Treeview):
    major = ent_major.get()
    id = ent_id.get()
    name = ent_name.get()

    db = DBconn(DB_FILE)

    main_query = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
    
    conditions = []
    values = []
    if major and major != "전체학과":
        conditions.append("B.명칭 like ?")
        values.append(f"%{major}%")
    if id:
        conditions.append("A.학번 like ?")
        values.append(f"%{id}%")
    if name:
        conditions.append("A.이름 like ?")
        values.append(f"%{name}%")
    
    if conditions:
        main_query += " where "
        main_query += " and ".join(conditions)
    main_query += " order by 학번"
    
    db.cursor.execute(main_query, values)
    result = db.cursor.fetchall()

    for i in tree.get_children():
        tree.delete(i)
    for r in result:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))


def onselect_tree(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, btn_del:tk.Button):
    node = tree.focus()
    if not node:
        return
    
    values = tree.item(node, "values")
    if len(values) < 4:
        return
    name, id, major, state = values
    
    db = DBconn(DB_FILE)
    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    query1 = "select A.학번, A.이름, A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학과 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()
    id, name, email, major, state = result1
    
    details = [id, name, email, major, state]
    r_ents = [r_id, r_name, r_email, r_major, r_state]
    for ent, detail in zip(r_ents, details):
        if not ent in (r_major, r_state):
            ent.config(state="normal")
            ent.delete(0, tk.END)
            ent.insert(0, detail)
            ent.config(state="disabled")
        else:
            ent.config(state="normal")
            ent.delete(0, tk.END)
            ent.insert(0, detail)
            ent.config(state="disabled")
    
    if current_user["role"] == "admin":
        r_email.config(state="normal")
        r_major.config(state="readonly")
        r_state.config(state="readonly")

    btn_del.config(state="normal")


def onclick_add(
    t_major:ttk.Combobox,
    t_id:tk.Entry,
    t_name:tk.Entry,
    r_id:tk.Entry,
    r_name:tk.Entry,
    r_email:tk.Entry,
    r_major:ttk.Combobox,
    r_state:ttk.Combobox,
    tree:ttk.Treeview
):
    tops = [t_major, t_id, t_name]
    rights = [r_id, r_name, r_email, r_major, r_state]

    for t in tops:
        if t in t_major:
            t.current(0)
        else:
            t.delete(0, tk.END)

    for r in rights:
        if r in (r_major, r_state):
            r.config(state="normal")
            r.current(0)
        else:
            r.config(state="normal")
            r.delete(0, tk.END)

    tree.focus("")
    tree.selection_remove(tree.selection())

    
def onclick_save(
    tree:ttk.Treeview,
    r_id:tk.Entry,
    r_name:tk.Entry,
    r_email:tk.Entry,
    r_major:ttk.Combobox,
    r_state:ttk.Combobox,
):
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()
    rights = [id, name, email, major, state]

    db = DBconn(DB_FILE)

    query1 = "select 학과코드 from 학과정보 where 명칭 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()
    major_code = result1[0]

    node = tree.focus()

    if node:
        # 수정
        update_query = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ? where 학번 = ?"
        db.cursor.execute(update_query, (email, major_code, state, id,))
        db.conn.commit()

    else:
        # 추가
        query2 = "select count(*) from 학생정보 where 학번 = ?"
        db.cursor.execute(query2, (id,))
        result2 = db.cursor.fetchone()
        if len(id) != 5 and result2[0] == 0:
            messagebox.showerror("비정상적인 값", "학번 입력 오류")
            return
        
        if len(name) < 2:
            messagebox.showerror("비정상적인 값", "이름 입력 오류")
            return
        
        if len(email) < 8:
            messagebox.showerror("비정상적인 값", "이메일 입력 오류")
            return
        
        query3 = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query3, (major,))
        result3 = db.cursor.fetchone()
        if not result3:
            messagebox.showerror("비정상적인 값", "학과 입력 오류")
            return
        
        if state in ("재학", "졸업", "휴학", "퇴학"):
            messagebox.showerror("비정상적인 값", "상태 입력 오류")
            return
        
        insert_query = "insert into 학생정보 (학번, 이름, 이메일, 학과, 상태) value (?, ?, ?, ?, ?)"
        db.cursor.execute(insert_query, (id, name, email, major_code, state,))
        db.conn.commit()
        
    query4 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
    db.cursor.execute(query4)
    result4 = db.cursor.fetchall()
    for i in tree.get_children():
        tree.delete(i)
    for r in result4:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))


def onclick_delete(
    tree:ttk.Treeview,
    btn_del:tk.Button,
    r_id:tk.Entry,
    r_name:tk.Entry,
    r_email:tk.Entry,
    r_major:ttk.Combobox,
    r_state:ttk.Combobox,
):
    node = tree.focus()
    if not node:
        return

    values = tree.item(node, "values")
    if not values or len(values) < 4:
        return
    name, id, major, state = values

    db = DBconn(DB_FILE)

    delete_query = "delete from 학생정보 where 학번 = ?"
    db.cursor.execute(delete_query, (id,))
    db.conn.commit()

    rights = [r_id, r_name, r_email, r_major, r_state]
    for r in rights:
        if r in (r_id, r_name):
            r.config(state="normal")
            r.delete(0, tk.END)
            r.config(state="disabled")
        else:
            r.config(state="normal")
            r.delete(0, tk.END)

    btn_del.config(state="disabled")