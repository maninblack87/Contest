import tkinter as tk
from tkinter import ttk
import json

from db.dbconn import DBconn
from config import DB_FILE, CURRENT_USER

def onselect_tree(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    id = r_id.get()

    print("좌측 목록 선택 이벤트 시작")
    print(f"id = {id}")

    node = tree.focus()
    if not node:
        return
    
    values = tree.item(node, "values")
    if not values or len(values) != 4:
        return
    
    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)
    
    query1 = "select A.학번, A.이름, A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
    db.cursor.execute(query1, (values[1],))
    result1 = db.cursor.fetchone()

    r_id.config(state="normal")
    r_id.delete(0, tk.END)
    r_id.insert(0, result1[0])
    r_id.config(state="disabled")
    r_name.config(state="normal")
    r_name.delete(0, tk.END)
    r_name.insert(0, result1[1])
    r_name.config(state="disabled")
    r_email.config(state="normal")
    r_email.delete(0, tk.END)
    r_email.insert(0, result1[2])
    r_major.config(state="normal")
    r_major.delete(0, tk.END)
    r_major.insert(0, result1[3])
    r_major.config(state="readonly")
    r_state.config(state="normal")
    r_state.delete(0, tk.END)
    r_state.insert(0, result1[4])
    r_state.config(state="readonly")

    if current_user["role"] != "admin":
        r_email.config(state="disabled")
        r_major.config(state="disabled")
        r_state.config(state="disabled")

    print("좌측 목록 선택 이벤트 종료")