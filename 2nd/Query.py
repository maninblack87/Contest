# Query.py
import tkinter as tk
from tkinter import ttk

import Connect

# 학생정보 테이블 검색 함수
def searchStudentInfo(major, std_id, name, tree):

    # 데이터베이스 연결
    db_connection = Connect.connect_to_mysql()

    # 데이터베이스에 쿼리를 보낼 커서 생성
    cursor = db_connection.cursor()

    # 기본 쿼리 생성(학생정보 테이블의 모든 정보를 조회함)
    query = """
        SELECT A.이름, A.학번, B.명칭, A.상태
        FROM 학생정보 A LEFT JOIN 학과정보 B
        ON A.학과 = B.학과코드
        """
    conditions = []
    values = []

    # 입력한 조건에 따라 학생정보를 조회하는 쿼리로 수정
    if major != "전체":
        conditions.append("B.명칭 LIKE %s")
        values.append(f"%{major}%")
    if std_id:
        conditions.append("A.학번 LIKE %s")
        values.append(f"%{std_id}%")
    if name:
        conditions.append("A.이름 LIKE %s")
        values.append(f"%{name}%")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY A.학번"

    # 쿼리를 실행해서 데이터 생성
    cursor.execute(query, values)
    rows = cursor.fetchall()

    # 현재 생선된 데이터를 트리에 추가하기 전에, 기존에 있던 데이터를 전부 삭제
    for i in tree.get_children():
        tree.delete(i)

    # 현재 생성된 데이터를 트리에 추가
    for row in rows:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))


# 추가버튼 클릭 함수
def click_add_button(combo1:ttk.Combobox, ent2:tk.Entry, ent3:tk.Entry, ent4:tk.Entry, ent5:tk.Entry, ent6:tk.Entry, combo7:ttk.Combobox, combo8:ttk.Combobox):

    # 입력창 활성화
    ent4.config(state="normal")
    ent5.config(state="normal")
    ent6.config(state="normal")

    # 입력창 텍스트 공백화(초기화)
    combo1.current(0)
    ent2.delete(0, tk.END)
    ent3.delete(0, tk.END)
    ent4.delete(0, tk.END)
    ent5.delete(0, tk.END)
    ent6.delete(0, tk.END)
    combo7.current(0)
    combo8.current(0)