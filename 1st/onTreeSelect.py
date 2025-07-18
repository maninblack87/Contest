import tkinter as tk
from tkinter import messagebox

import Connect

def on_tree_select(tree, stdnum, name, email, major, state, delete_btn, current_user):
    
    # 선택한 트리의 아이디 가져오기
    selected_item = tree.focus()

    if not selected_item:
        return
    
    # 선택한 트리의 값만 가져오기
    values = tree.item(selected_item, "values")

    if not values or len(values) < 4:
        return
    
    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()
    
    # SQL문으로 학생정보와 학과정보를 병합시키기
    query = "SELECT * FROM 학생정보 WHERE 학생정보.학번 = %s"
    cursor.execute(query, (values[1],))
    selected = cursor.fetchone()
    
    # 학번 채우기
    stdnum.config(state="normal")
    stdnum.delete(0, tk.END)
    stdnum.insert(0, selected[0])
    stdnum.config(state="disabled")

    # 이름 채우기
    name.config(state="normal")
    name.delete(0, tk.END)
    name.insert(0, selected[1])
    name.config(state="disabled")

    # 이메일 채우기
    email.config(state="normal")
    email.delete(0, tk.END)
    email.insert(0, selected[2])
    email.config(state="disabled")

    # 학과의 명칭을 '학과정보'로부터 찾기
    query = "SELECT 명칭 FROM 학과정보 WHERE 학과정보.학과코드 = %s"
    cursor.execute(query, (selected[3],))
    major_name = cursor.fetchone()
    # 학과 채우기
    major.set(major_name)

    # 상태 채우기
    state.set(selected[4])

    # 사용자가 USER일 경우
    if current_user['role'] == 'USER':
        stdnum.config(state="disabled")
        name.config(state="disabled")

    # 사용자가 ADMIN일 경우
    if current_user['role'] == 'ADMIN':
        delete_btn.config(state="normal")