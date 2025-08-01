# Query.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

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


# 저장버튼 클릭 함수
def click_save_button(std_id:tk.Entry, name:tk.Entry, email:tk.Entry, major:ttk.Combobox, state:ttk.Combobox, tree:ttk.Treeview):

    # 1. 데이터베이스 연결, 커서 생성
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 2. 모든 제약조건을 체크하고 학생 정보 추가 수행
    if check_for_save(std_id.get(), name.get(), email.get(), major.get(), state.get()):

        # 입력된 학과 명칭을 학생정보 테이블의 학과 번호로 변환
        query1 = """
            SELECT 학과코드 
            FROM 학과정보
            WHERE 명칭 = %s
            """
        cursor.execute(query1, (major.get(),))
        result = cursor.fetchone()
        major_code = result[0]

        # 추가 or 수정 여부 확인
        query1 = "SELECT COUNT(*) FROM 학생정보 WHERE %s = 학번"
        cursor.execute(query1, (std_id.get(),))
        result = cursor.fetchone()
        existing_id = result[0]

        # 추가/수정 여부에 따라 SQL문 생성->실행->결과도출
        if existing_id > 0:
            query2 = """
                UPDATE 학생정보
                SET 학번 = %s, 이름 = %s, 이메일 = %s, 학과 = %s, 상태 = %s
                WHERE 학번 = %s
                """
            cursor.execute(query2, (std_id.get(), name.get(), email.get(), major_code, state.get(), std_id.get(),))
            db_connection.commit()

            messagebox.showinfo("수정 성공", "학생을 성공적으로 수정했습니다")
        else:
            query2 = """
                INSERT INTO 학생정보(학번, 이름, 이메일, 학과, 상태)
                VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(query2, (std_id.get(), name.get(), email.get(), major_code, state.get()))
            db_connection.commit()

            messagebox.showinfo("추가 성공", "학생을 성공적으로 추가했습니다")

    else:

        # 에러창 생성 : 추가 실패
        messagebox.showerror("학생 정보 추가/수정 오류", "비정상적인 값")


    # 3. 학생목록 비우기
    for item in tree.get_children():
        tree.delete(item)

    # 4. 수정 or 추가 후, 입력란 모두 비우기
    std_id.config("normal")
    std_id.delete(0, tk.END)
    std_id.config(state="disabled")
    
    name.config("normal")
    name.delete(0, tk.END)
    name.config(state="disabled")

    email.delete(0, tk.END)

    major.set("선택")

    state.set("")

    # 5. 데이터베이스 연결 종료
    db_connection.close()


# 식제 함수
def click_delete_button(std_id:tk.Entry, name:tk.Entry, email:tk.Entry, major:ttk.Combobox, state:ttk.Combobox, delete_btn:tk.Button, tree:ttk.Treeview):
    
    # 데이터베이스 연결, 커서 생성
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 학생정보에서 해당하는 정보 삭제하기(SQL문으로)
    query = "DELETE FROM 학생정보 WHERE 학번 = %s"
    cursor.execute(query, (std_id.get(),))
    db_connection.commit()

    # 학생목록 비우기
    for item in tree.get_children():
        tree.delete(item)

    # 입력란 모두 비우기
    std_id.config(state="normal")
    std_id.delete(0, tk.END)
    std_id.config(state="disabled")

    name.config(state="normal")
    name.delete(0, tk.END)
    name.config(state="disabled")

    email.delete(0, tk.END)

    major.set("선택")

    state.set("")

    # 데이터베이스 연결 종료
    db_connection.close()



# 추가/수정 전 제약조건 설정 함수
def check_for_save(std_id:str, name:str, email:str, major:str, state:str):

    # >> 조건 - 학번 1 : 학번은 5자리 숫자
    check_id1 = re.fullmatch(r'\d{5}', std_id)

    # >> 조건 - 학번 2 : (데이터베이스에 있는) 기존 학번과 중복 금지
    connection = Connect.connect_to_mysql()     # 데이터베이스 연결
    cursor = connection.cursor()                # 커서 생성
    query = "SELECT 학번 FROM 학생정보"           # 조회 쿼리 생성
    cursor.execute(query)                       # 조회 쿼리 실행
    result = cursor.fetchall()                  # 조회 결과
    existing_ids = {str(row[0]) for row in result}  # 리스트화
    connection.close()                          # 커넥션 종료

    check_id2 = std_id not in existing_ids

    # >> 조건 - 이름 : 최소 2글자 이상
    check_name = len(name) >= 2

    # >> 조건 - 이메일 : 최소 8글자 이상
    check_email = len(email) >= 8

    # >> 조건 - 학과 : "선택" 항목 외 다른 항목이 선택되여야 함
    check_major = major != "선택"

    # >> 조건 - 상태 : (추가할 때 상태는 항상) "재학"만 선택되어있어야 함
    check_state = state == "재학"

    if check_id1 and check_id2 and check_name and check_email and check_major and check_state:
        return True
    else:
        return False