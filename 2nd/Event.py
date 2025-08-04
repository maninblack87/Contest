import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import Connect

def on_tree_select(tree, std_id:tk.Entry, name:tk.Entry, email:tk.Entry, major:ttk.Combobox, state:ttk.Combobox, current_user, delete_button:tk.Button):
    """
    tree(ttk.Treeview)에서 학생 항목을 선택하면 해당 학생의 정보를 우측 입력란에 표시하는 함수

    tree : Treeview에 의해 만틀어진 뷰
    std_id,name,email,major,state : 학생의 데이터들의 입력칸
    current_user : CurrentUser.json으로부터 불러온 사용자 정보
    delete_button : 삭제 버튼
    """

    # 선택한 트리의 아이디 가져오기
    selected_item = tree.focus()
    # >> 예외
    if not selected_item:
        return

    # 선택한 트리의 값만 가져오기
    values = tree.item(selected_item, "values")

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()
    
    # 쿼리를 보낼 커서 생성
    cursor = db_connection.cursor()

    # SQL문으로 뷰를 생성 : 학생정보와 학과정보를 병합시킴
    query = """
        SELECT * 
        FROM (SELECT A.학번, A.이름, A.이메일, B.명칭, A.상태 
            FROM 학생정보 A JOIN 학과정보 B
            WHERE A.학과 = B.학과코드) VIEW
        WHERE VIEW.학번 = %s
    """
    cursor.execute(query, (values[1],))
    selected_std_info = cursor.fetchone()

    # 선택한 트리의 값을 입력란에 표시
    # # 이때 각 입력란(Entry)는 **일시적으로** 활성화시켜야 됨
    # 1) 학번
    std_id.config(state="normal")
    std_id.delete(0, tk.END)
    std_id.insert(0, selected_std_info[0])
    std_id.config(state="disabled")
    # 2) 이름
    name.config(state="normal")
    name.delete(0, tk.END)
    name.insert(0, selected_std_info[1])
    name.config(state="disabled")
    # 3) 이메일
    email.config(state="normal")
    email.delete(0, tk.END)
    email.insert(0, selected_std_info[2])
    email.config(state="disabled")
    # 4) 학과(명칭)
    major.set(selected_std_info[3])
    # 5) 상태
    state.set(selected_std_info[4])

    # 사용자의 권한 정보에 따라 권한 부여/제한
    # 사용자 권한이 USER
    # >> 학생 추가 기능 제한 : 학생의 학번과 이름을 비활성화시킨다.
    if current_user["role"] == 'user':
        std_id.config(state="disabled")
        name.config(state="disabled")
    # 사용자 권한이 ADMIN
    # >> 삭제 기능 부여
    if current_user["role"] == 'admin':
        delete_button.config(state="normal")