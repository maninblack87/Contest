import tkinter as tk
from tkinter import ttk
import json

from db.DBconn import DBconn
from config import DB_FILE, CURRENT_USER


def onselect_tree(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, btn_del:tk.Button):

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 선택한 노드
    node = tree.focus()
    if not node:
        return

    # 선택한 노드의 값
    # >> 노드 : [이름, 학번, 학과, 상태]
    values = tree.item(node, "values")
    if not values:
        return
    id = values[1]
    
    # (해당 노드의 학과를 가지고) 데이터베이스에서 필요한 데이터 조회
    query1 = "select A.학번, A.이름, A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B where A.학번 = ?"
    db.cursor.execute(query1, (id,))
    result1 = db.cursor.fetchone()
    db_id = result1[0]
    db_name = result1[1]
    db_email = result1[2]
    db_major = result1[3]
    db_state = result1[4]

    # 우측 상세정보에 표시
    r_id.config(state="normal")
    r_id.delete(0, tk.END)
    r_id.insert(0, db_id)
    r_id.config(state="disabled")
    r_name.config(state="normal")
    r_name.delete(0, tk.END)
    r_name.insert(0, db_name)
    r_name.config(state="disabled")
    r_email.config(state="normal")
    r_email.delete(0, tk.END)
    r_email.insert(0, db_email)
    r_major.config(state="normal")
    r_major.delete(0, tk.END)
    r_major.insert(0, db_major)
    r_major.config(state="readonly")
    r_state.config(state="normal")
    r_state.delete(0, tk.END)
    r_state.insert(0, db_state)
    r_state.config(state="readonly")
    
    if current_user["role"] != "admin":
        r_email.config(state="disabled")
        r_major.config(state="disabled")
        r_state.config(state="disabled")
        # (관리자 권한이 admin이면) 삭제 버튼 활성화
        btn_del.config(state="normal")