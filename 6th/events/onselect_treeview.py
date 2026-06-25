import tkinter as tk
from tkinter import ttk
import json

from db.DBconnection import DBconnection
from config import DB_FILE, CURRENT_USER

def onselect_treeview(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, del_btn:tk.Button):

    # 트리뷰에서 선택된 노드
    selected_node = tree.selection()
    if not selected_node:
        del_btn.config(state="disabled")
        return
    node = selected_node[0]
    
    # 선택 된 노드에서 값 가져오기
    values = tree.item(node, "values")
    if not values:
        return
    
    # DB 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 현재 사용자 정보
    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 선택 된 노드와 일치하는 DB정보 가져오기
    query1 = "select A.학번, A.이름, A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
    db.cursor.execute(query1, (values[1],))
    result1 = db.cursor.fetchone()

    # 우측 상세정보 초기화
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

    # 현재 사용자 권한이 "user"이면 - 입력 제한
    if current_user["role"] == "user":
        r_email.config(state="disabled")
        r_major.config(state="disabled")
        r_state.config(state="disabled")
        del_btn.config(state="disabled")

    if current_user["role"] == "admin":
        # 삭제 버튼 활성화
        del_btn.config(state="normal")