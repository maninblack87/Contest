import tkinter as tk
from tkinter import messagebox

import Connect
from CheckAllowedAddCondition import check_allowed_add_condition

# 추가 버튼 클릭시
def on_click_add(entry1, entry2, entry3, entry4, entry5, combo2, combo3):

    # 입력창 활성화
    entry3.config(state="normal")
    entry4.config(state="normal")
    entry5.config(state="normal")

    # 입력창 텍스트 공백으로 초기화
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    entry4.delete(0, tk.END)
    entry5.delete(0, tk.END)
    combo2.current(0)
    combo3.current(0)


# 저장 버튼 클릭시 -> 수정함수 or 추가함수를 수행시킴
def save_start(student_id, name, email, major, state, delete_btn, tree):

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 넘겨진 데이터가 추가되는지 혹은 수정되는지 체크
    query1 = "SELECT COUNT(*) FROM 학생정보 WHERE 학생정보.학번 = %s"
    cursor.execute(query1, (student_id,))
    check1 = cursor.fetchone()

    if check1[0] > 0:
        messagebox.showinfo("알림", "수정은 아직 불가능합니다")
    else:
        add(student_id, name, email, major, state, tree)

    # 입력란 모두 비우기
    student_id.config(state="normal")
    student_id.delete(0, tk.END)
    student_id.config(state="disabled")

    name.config(state="normal")
    name.delete(0, tk.END)
    name.config(state="disabled")

    email.delete(0, tk.END)

    major.set("선택")

    state.set("")

    delete_btn.config(state="disabled")


# 추가
def add(student_id, name, email, major, state, tree):

    if check_allowed_add_condition(student_id, name, email, major, state):

        # 데이터베이스 연결
        db_connection = Connect.connect_to_mysql()
        cursor = db_connection.cursor()

        # 쿼리1) 입력받은 학과명으로 학과코드를 반환
        query1 = "SELECT * FROM 학과정보 WHERE 학과정보.명칭 = %s"
        cursor.execute(query1, (major, ))
        major_code = cursor.fetchone()[0]

        # 쿼리2) 학생정보에 정보 추가하기
        query2 = "INSERT INTO 학생정보(학번, 이름, 이메일, 학과, 상태) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query2, (student_id, name, email, major_code, state))

        db_connection.commit()

        # 알림창 : 추가 성공
        messagebox.showinfo("추가 성공", "학생을 성공적으로 추가했습니다")

    else:

        messagebox.showerror("비정상적인 값", "비정상적인 값입니다")

    # 학생목록(Treeview) 비우기
    for item in tree.get_children():
        tree.delete(item)


# 삭제
def delete(student_id, name, email, major, state, delete_btn, tree):

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 쿼리1) 학생정보에 정보 삭제하기
    query1 = "DELETE FROM 학생정보 WHERE 학번 = %s"
    cursor.execute(query1, (student_id.get(), ))

    # 변경사항 저장
    db_connection.commit()

    # 연결 종료
    db_connection.close()

    # 학생목록(Treeview) 비우기
    for item in tree.get_children():
        tree.delete(item)

    # 입력란 모두 비우기
    student_id.config(state="normal")
    student_id.delete(0, tk.END)
    student_id.config(state="disabled")

    name.config(state="normal")
    name.delete(0, tk.END)
    name.config(state="disabled")

    email.delete(0, tk.END)

    major.set("선택")

    state.set("")

    delete_btn.config(state="disabled")