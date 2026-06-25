# search.py
import tkinter as tk
from tkinter import ttk
import json

from db.dbconnection import DBconnection
from config import DB_FILE

def search(t_major:ttk.Combobox, t_id:tk.Entry, t_name:tk.Entry, treeview:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    major = t_major.get()
    id = t_id.get()
    name = t_name.get()

    print("test1")

    db = DBconnection(DB_FILE)
    db.connect()

    print("test2")

    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    print(f"test3: {current_user}")

    conditions = []
    values = []
    query1 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"

    if major and major != "전체학과":
        conditions.append("B.명칭 like ?")
        values.append(f"%{major}%")
        print(f"test4: 입력 학과 - {major}")
    if id:
        conditions.append("A.학번 like ?")
        values.append(f"%{id}%")
        print(f"test4: 입력 학번 - {id}")
    if name:
        conditions.append("A.이름 like ?")
        values.append(f"%{name}%")
        print(f"test4: 입력 이름 - {name}")

    if conditions:
        query1 += " where " + " and ".join(conditions)
    query1 += " order by A.학번"
    print(f"test5: query문 - {query1}")
    
    db.cursor.execute(query1, values)
    result1 = db.cursor.fetchall()

    print(f"test6 : result1 - {result1}")

    for i in treeview.get_children():
        treeview.delete(i)
    for r in result1:
        treeview.insert("", "end", values=(r[0], r[1], r[2], r[3]))

    print("test7")

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

    print("test8")

    if current_user["role"] == "user":
        r_email.config("disabled")
        r_major.config("disabled")
        r_state.config("disabled")