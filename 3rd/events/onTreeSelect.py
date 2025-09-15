# events/onTreeSelect.py
import tkinter as tk
from tkinter import messagebox, ttk
from config import DB_FILE

from sqlite.DBconnection import DBconnection

def on_tree_select(tree:ttk.Treeview, id:tk.Entry, name:tk.Entry, email:tk.Entry, major:ttk.Combobox, state:ttk.Combobox):

    # 선택한 (트리)노드 아이디 가져오기
    node = tree.focus()

    # 만약, 선택한 노드가 없으면 즉시 해당 함수 탈출
    if not node:
        return
    
    # 선택한 노드의 값만 가져오기
    values = tree.item(node, "values")

    # 데이터 유효성 검사
    if not values or len(values) < 4:
        messagebox.showerror("데이터 오류 발생", "유효한 데이터가 아닙니다")
        return

    # 데이터베이스 연결
    db = DBconnection(DB_FILE)
    db.connect()

    # 학생정보/학과정보 DB로부터 선택된 노드의 값으로 학생정보 가져오기
    query = """
        select A.학번, A.이름, A.이메일, B.명칭, A.상태
        from 학생정보 A join 학과정보 B
        on A.학과 = B.학과코드
        where A.학번 = ?
        """
    db.cursor.execute(query, (values[1],))
    result = db.cursor.fetchone()

    # 입력창에 DB로부터 가져온 학생정보를 표시
    # 1. 학번
    id.config(state="normal")
    id.delete(0, tk.END)
    id.insert(0, result[0])
    id.config(state="disabled")
    # 2. 이름
    name.config(state="normal")
    name.delete(0, tk.END)
    name.insert(0, result[1])
    name.config(state="disabled")
    # 3. 이메일
    email.config(state="normal")
    email.delete(0, tk.END)
    email.insert(0, result[2])
    email.config(state="disabled")
    # 4. 학과
    major.set(result[3])
    # 5. 상태
    state.set(result[4])