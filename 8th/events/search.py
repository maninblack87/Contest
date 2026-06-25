import tkinter as tk
from tkinter import ttk

from config import DB_FILE
from db.dbconn import DBconn

def search(t_major:ttk.Combobox, t_id:tk.Entry, t_name:tk.Entry, tree:ttk.Treeview):
    major = t_major.get()
    id = t_id.get()
    name = t_name.get()

    db = DBconn(DB_FILE)
    db.connect()

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
    query1 += " order by A.학번"

    db.cursor.execute(query1, values)
    result1 = db.cursor.fetchall()

    # 트리뷰 초기화 및 갱신
    for i in tree.get_children():
        tree.delete(i)
    for r in result1:
        tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))