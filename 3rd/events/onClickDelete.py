# events/onClickDelete.py
import tkinter as tk
from tkinter import ttk, messagebox

from query import delStudent
from sqlite.DBconnection import DBconnection
from config import DB_FILE

def on_click_delete(
        id: tk.Entry,
        name: tk.Entry,
        email: tk.Entry,
        major: ttk.Combobox,
        state: ttk.Combobox,
        tree:ttk.Treeview, 
        del_btn:tk.Button
        ):
    
    # 입력창의 값만 별도 정의
    id_val = id.get()

    # 쿼리문 생성 및 실행(삭제)
    delStudent.del_student(id_val)

    # 삭제 성공 메세지
    messagebox.showinfo("학생 삭제 성공", "학생 삭제에 성공했습니다")

    # 삭제 버튼 비활성화
    del_btn.config(state="disabled")

    # Treeview 목록 초기화
    for item in tree.get_children():
        tree.delete(item)

    # Treeview 데이터베이스에 갱신
    db = DBconnection(DB_FILE)
    db.connect()
    query = """
        select A.이름, A.학번, B.명칭, A.상태
        from 학생정보 A join 학과정보 B
        on A.학과 = B.학과코드
    """
    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    # 입력창 초기화
    # >> 학번
    id.config(state="normal")
    id.delete(0, tk.END)
    id.config(state="disabled")
    # >> 이름
    name.config(state="normal")
    name.delete(0, tk.END)
    name.config(state="disabled")
    # >> 이메일
    email.delete(0, tk.END)
    # >> 학과
    major.current(0)
    # >> 상태
    state.current(0)

    # 갱신된 Treeview 목록 표시
    for row in rows:
        tree.insert("", "end", values=row)

    return