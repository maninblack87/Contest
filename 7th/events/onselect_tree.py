import tkinter as tk
from tkinter import ttk
import json

from DB.DBconn import DBconn
from config import DB_FILE, CURRENT_USER

def onselect_tree(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):

    print("트리 목록 선택 함수 시작")

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 내장 함수
    # 우측 상세 정보 표시/초기화 처리 함수
    def display_detail(obj:tk.Entry|ttk.Combobox, role:str, value:str=None, must_disabled:bool=False, is_readonly:bool=False):
        obj.config(state="normal")
        obj.delete(0, tk.END)
        if value:
            obj.insert(0, value)
        if is_readonly:
            obj.config(state="readonly")
        if role != "admin":
            obj.config(state="disabled")
        if must_disabled == True:
            obj.config(state="disabled")

    node = tree.focus()
    if not node:
        return

    values = tree.item(node, "values")
    if not values and len(values) != 4:
        return
    
    query1 = "select A.학번, A.이름, A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
    db.cursor.execute(query1, (values[1],))
    result1 = db.cursor.fetchone()
    res_id = result1[0]
    res_name = result1[1]
    res_email = result1[2]
    res_major = result1[3]
    res_state = result1[4]

    # 우측 상세 정보에 표시
    display_detail(r_id, current_user["role"], res_id, must_disabled=True)
    display_detail(r_name, current_user["role"], res_name, must_disabled=True)
    display_detail(r_email, current_user["role"], res_email)
    display_detail(r_major, current_user["role"], res_major, is_readonly=True)
    display_detail(r_state, current_user["role"], res_state, is_readonly=True)

    print("트리 목록 선택 함수 종료(성공)")