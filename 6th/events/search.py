import tkinter as tk
from tkinter import ttk
import json

from config import DB_FILE, CURRENT_USER
from db.DBconnection import DBconnection

def search(t_major:ttk.Combobox, 
           t_id:tk.Entry, 
           t_name:tk.Entry, 
           tree:ttk.Treeview, 
           r_id:tk.Entry, 
           r_name:tk.Entry, 
           r_email:tk.Entry, 
           r_major:ttk.Combobox, 
           r_state:ttk.Combobox,
           del_btn:tk.Button
           ):
    
    major = t_major.get()
    id = t_id.get()
    name = t_name.get()

    db = DBconnection(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    query1 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
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
        query1 += " where "
        query1 += " and ".join(conditions)
    query1 += " order by 학번"

    db.cursor.execute(query1, values)
    result1 = db.cursor.fetchall()

    for node in tree.get_children():
        tree.delete(node)
    for r in result1:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))
    
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
    r_major.config(state="readonly")
    
    if current_user["role"] == "user":
        r_email.config(state="disabled")
        r_major.config(state="disabled")
        r_state.config(state="disabled")

    del_btn.config(state="disabled")