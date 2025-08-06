# Query.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import json

import Connect
import Router

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

    # 데이터베이스 연결, 커서 생성
    db_connection = Connect.connect_to_mysql()
    cursor = db_connection.cursor()

    # 수정 혹은 추가 여부를 체크해서 check_for_save()함수에 반영시킨다
    # >> 참고 : check_for_save()함수에는 추가할때만 체크해야하는 부분이 있음
    # >> 수정 여부 체크방법 : 추가버튼을 누를 때 활성화되는 입력란을 통해 체크 가능
    if std_id.cget("state")=="normal" and name.cget("state")=="normal" and email.cget("state")=="normal":
        is_modify = False
    else:
        is_modify = True

    # 모든 제약조건을 체크하고 학생 정보 추가 수행
    if check_for_save(std_id.get(), name.get(), email.get(), major.get(), state.get(), is_modify):

        # 추가 or 수정 여부 확인
        query1 = "SELECT COUNT(*) FROM 학생정보 WHERE 학번 = %s"
        cursor.execute(query1, (std_id.get(),))
        result = cursor.fetchone()
        existing_id = result[0]

        # 미리 입력된 학과 명칭을 학생정보 테이블의 학과 번호로 변환
        # >> 다음에 수행될 수정/추가 SQL문에의해 참조됨
        query1 = """
            SELECT 학과코드 
            FROM 학과정보
            WHERE 명칭 = %s
            """
        cursor.execute(query1, (major.get(),))
        result = cursor.fetchone()
        major_code = result[0]

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
            cursor.execute(query2, (std_id.get(), name.get(), email.get(), major_code, state.get(),))
            db_connection.commit()

            messagebox.showinfo("추가 성공", "학생을 성공적으로 추가했습니다")

    else:

        # 에러창 생성 : 추가 실패
        messagebox.showerror("학생 정보 추가/수정 오류", "비정상적인 값")


    # 학생목록 비우기
    for item in tree.get_children():
        tree.delete(item)

    # 갱신된 학생목록으로 다시 표시하기
    # >> (변경되었을) 학생정보 테이블 다시 조회
    query = """
        SELECT A.이름, A.학번, B.명칭, A.상태
        FROM 학생정보 A
        LEFT JOIN 학과정보 B ON A.학과 = B.학과코드
        ORDER BY A.학번
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    # >> 해당 조회된 정보들을 학생목록에 표시
    for row in rows:
        tree.insert('', tk.END, values=row)

    # 수정 or 추가 후, 입력란 모두 비우기
    std_id.config(state="normal")
    std_id.delete(0, tk.END)
    std_id.config(state="disabled")
    
    name.config(state="normal")
    name.delete(0, tk.END)
    name.config(state="disabled")

    email.delete(0, tk.END)
    email.config(state="disabled")

    major.set("선택")

    state.set("")

    # 데이터베이스 연결 종료
    db_connection.close()


# 추가/수정 전 제약조건 설정 함수
def check_for_save(std_id:str, name:str, email:str, major:str, state:str, is_modify:bool):

    # >> 조건 - 학번 1 : 학번은 5자리 숫자
    if not re.fullmatch(r'\d{5}', std_id):
        messagebox.showerror("학번 입력 오류", "학번은 5자리 숫자로 입력되어야 합니다")
        return False
    
    # >> 조건 - 학번 2 : 
    # >> >> 학번 2-1 : 수정이 아닐 경우 아래 조건문 실행
    if not is_modify:

        # >> >> 학번 2-2 : (데이터베이스에 있는) 기존 학번과 중복이 없어야 학생 정보 추가가 가능함
        connection = Connect.connect_to_mysql()     # 데이터베이스 연결
        cursor = connection.cursor()                # 커서 생성
        query = "SELECT 학번 FROM 학생정보"           # 조회 쿼리 생성
        cursor.execute(query)                       # 조회 쿼리 실행
        result = cursor.fetchall()                  # 조회 결과
        existing_ids = {str(row[0]) for row in result}  # 리스트화
        connection.close()                          # 커넥션 종료

        # 기존 데이터베이스에 학번이 있으면 해당 정보가 추가되지 않도록 False값을 반환한다
        if std_id in existing_ids:
            messagebox.showerror("학번 입력 오류", "기존에 있는 학번으로 추가를 시도하셨습니다")
            return False

    # >> 조건 - 이름 : 최소 2글자 이상
    if not len(name) >= 2:
        messagebox.showerror("이름 입력 오류", "이름은 2글자 이상 이어야 합니다")
        return False

    # >> 조건 - 이메일 : 최소 8글자 이상
    if not len(email) >= 8:
        messagebox.showerror("이메일 입력 오류", "이메일은 8글자 이상이어야 합니다")
        return False

    # >> 조건 - 학과 : "선택" 항목 외 다른 항목이 선택되여야 함
    if major == "선택":
        messagebox.showerror("학과 입력 오류", "학과를 선택하셔야 합니다")
        return False

    # >> 조건 - 상태 : (추가할 때 상태는 항상) "재학"만 선택되어있어야 함
    if not state == "재학":
        messagebox.showerror("상태 입력 오류", "상태는 재학이여야만 합니다")
        return False

    # 모든 조건에 맞아서 여기까지 온다면 True값으로 반환한다
    return True


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

    # 갱신된 학생목록으로 다시 표시하기
    # >> (변경되었을) 학생정보 테이블 다시 조회
    query = """
        SELECT A.이름, A.학번, B.명칭, A.상태
        FROM 학생정보 A
        LEFT JOIN 학과정보 B ON A.학과 = B.학과코드
        ORDER BY A.학번
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    # >> 해당 조회된 정보들을 학생목록에 표시
    for row in rows:
        tree.insert('', tk.END, values=row)

    # 입력란 모두 비우기
    std_id.config(state="normal")
    std_id.delete(0, tk.END)
    std_id.config(state="disabled")

    name.config(state="normal")
    name.delete(0, tk.END)
    name.config(state="disabled")

    email.config(state="disabled")

    major.set("선택")

    state.set("")

    # 데이터베이스 연결 종료
    db_connection.close()


# 비밀번호 변경 함수
def change_password(current_pw:str, new_pw:str, verify_new_pw:str):

    # 1. 로그인 사용자의 암호와 현재 암호에 입력한 암호가 같은지 비교
    # >>현재 로그인 중인 사용자 불러오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)
    
    # 2. 아래 조건이 만족되면, 암호가 변경되도록 한다
    # >> 조건1 : 현재 암호 값이 데이터베이스의 현재 사용자의 암호와 일치
    db_connection = Connect.connect_to_mysql()          # 데이터베이스 연결
    cursor = db_connection.cursor()                     # 커서 생성
    query = "SELECT 암호 FROM 업무사용자 WHERE 사번 = %s"  # 쿼리문 생성
    cursor.execute(query, (current_user["id"],))        # 쿼리 실행
    result = cursor.fetchone()                          
    db_user_pw = result[0]                              # 해당 데이터베이스 사용자 암호 저장
    # >> >> 조건1 수행
    check1 = current_pw == db_user_pw

    # >> 조건2 : 현재 암호에 입력된 값이 새 암호의 값과 달라야 됨
    check2 = current_pw != new_pw

    # >> 조건3 : 새 암호와 새 암호 확인에 입력된 값이 같아야 됨
    check3 = new_pw == verify_new_pw

    # >> 조건은 모두 충족되면 암호 변경을 실행한다
    if check1 and check2 and check3:

        # A-1 : 각 조건이 맞지 않으면 "실패한 조건이름(번호)"를 반환
        if not check1:
            return "failed_check1"
        elif not check2:
            return "failed_check2"
        elif not check3:
            return "failed_check3"

        # >> 암호 변경 수행
        query = "UPDATE 업무사용자 SET 암호 = %s WHERE 사번 = %s"
        cursor.execute(query, (new_pw, current_user["id"],))
        db_connection.commit()

        # 암호 변경 후에
        current_user["password"] = new_pw
        with open("CurrentUser.json", "w", encoding="utf-8") as f:
            json.dump(current_user, f, indent=4, ensure_ascii=False)

        # >> 성공 메세지
        messagebox.showinfo("암호저장 완료", "암호가 성공적으로 저장되었습니다")

        # A-2 : 모든 조건을 통과하면 "성공"을 반환
        return "success"