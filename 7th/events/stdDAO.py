# stdDAO.py는 students Data Access Object의 약자
# (주로) 학생정보 데이터베이스에 대해 DB 관련 작업만 따로 모아두기 위해 존재
import json
import tkinter as tk
from tkinter import messagebox, ttk

from config import CURRENT_USER, DB_FILE
from DB.DBconn import DBconn

def onclick_add(t_major:ttk.Combobox, t_id:tk.Entry, t_name:tk.Entry, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, tree:ttk.Treeview):

    print("추가 버튼 이벤트 시작")
    
    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] != "admin":
        messagebox.showerror("권한 오류", "해당 작업(추가 버튼 클릭)은 admin만 사용 가능합니다.")
        return
    
    print("test1")
    
    # 내장 함수
    # 우측 상세 정보 표시/초기화 처리 함수
    def display_detail(obj:tk.Entry|ttk.Combobox, role:str, value:str=None, must_disabled:bool=False, is_readonly:bool=False):
        print("추가 버튼 이벤트 내 내장함수 시작 : 우측 상세 정보 표시/초기화 처리 함수")
        obj.config(state="normal")
        obj.delete(0, tk.END)
        print("test1")
        if value:
            obj.insert(0, value)
        if is_readonly:
            obj.config(state="readonly")
        if role != "admin":
            obj.config(state="disabled")
        if must_disabled == True:
            obj.config(state="disabled")
        print("추가 버튼 이벤트 내 내장함수 종료 : 우측 상세 정보 표시/초기화 처리 함수")
    
    # 상단 검색 부분 처리(초기화)
    t_major.current(0)
    t_id.delete(0, tk.END)
    t_name.delete(0, tk.END)

    print("test2")

    # 우측 상세 정보 처리(초기화)
    display_detail(r_id, current_user["role"])
    display_detail(r_name, current_user["role"])
    display_detail(r_email, current_user["role"])
    display_detail(r_major, current_user["role"])
    display_detail(r_state, current_user["role"])
    r_major.current(0)
    r_state.current(0)

    # 트리뷰 선택 해제
    tree.focus("")

    print("추가 버튼 이벤트 종료")


def onclick_save(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()

    print("저장 버튼 이벤트 시작")

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] != "admin":
        messagebox.showerror("권한 오류", "해당 작업(저장 버튼 클릭)은 admin만 사용 가능합니다.")
        return
    
    print("test 1")

    # 데이터베이스가 필요없는 조건
    if len(id) != 5 or not id.isdigit():
        messagebox.showerror("비 정상적인 값", "학번은 5자리 숫자여야 합니다")
        return
    if len(name) < 2:
        messagebox.showerror("비 정상적인 값", "이름은 2글자 이상이어야 합니다")
        return
    if len(email) < 8:
        messagebox.showerror("비 정상적인 값", "이메일은 8글자 이상이어야 합니다")
        return
    
    print("test 2 : 데이터베이스가 필요없는 조건")


    try:
        query2 = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query2, (major,))
        result2 = db.cursor.fetchone()
        major_code = result2[0]

        print("test 3")

        # 데이터베이스가 필요한 조건
        db_majors = []
        query4 = "select 명칭 from 학과정보"
        db.cursor.execute(query4)
        result4 = db.cursor.fetchall()
        for r in result4:
            db_majors.append(r[0])
        if major not in db_majors:
            messagebox.showerror("비 정상적인 값", "데이터베이스에 포함된 학과명이어야 합니다")
            return
        
        print("test 4")

        # 추가/수정 여부
        if not tree.selection():
            # 추가의 경우
            query3 = "select * from 학생정보 where 학번 = ?"
            db.cursor.execute(query3, (id,))
            result3 = db.cursor.fetchone()
            if result3:
                messagebox.showerror("비 정상적인 값", "이미 존재하는 학번이기 때문에 추가가 불가능")
                return
            print("test 5: 추가1")
            
            if state != "재학":
                messagebox.showerror("비 정상적인 값", "상태는 재학이어야 합니다")
                return
            
            print("test 5: 추가2")
            
            insert_query = "insert into 학생정보 (학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"
            db.cursor.execute(insert_query, (id, name, email, major_code, state,))
            print("test 5: 추가3")
            db.conn.commit()
            print("test 5: 추가 종료")

        else:
            # 수정의 경우
            selected_node = tree.selection()
            node = selected_node[0]
            values = tree.item(node, "values")
            print("test 5: 수정1")

            query1 = "select A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
            db.cursor.execute(query1, (values[1],))
            result1 = db.cursor.fetchone()
            if email == result1[0] and major == result1[1] and state == result1[2]:
                return
            print("test 5: 수정2")
            
            update_query = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ? where 학번 = ?"
            db.cursor.execute(update_query, (email, major_code, state, id,))
            print("test 5: 수정3")
            db.conn.commit()
            print("test 5: 수정 종료")

        # 좌측 목록에 갱신
        query5 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query5)
        result5 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result5:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))
        print("test6")


    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    

    finally:
        db.close()
        print("저장 버튼 이벤트 종료")


def onclick_del(r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, tree:ttk.Treeview):
    id = r_id.get()

    db = DBconn(DB_FILE)
    db.connect()

    try:
        with open (CURRENT_USER, "r", encoding="utf-8") as f:
            current_user = json.load(f)

        if current_user["role"] != "admin":
            messagebox.showerror("권한 오류", "해당 작업(삭제 버튼 클릭)은 admin만 사용 가능합니다.")
            return
        
        delete_query = "delete from 학생정보 where 학번 = ?"
        db.cursor.execute(delete_query, (id,))
        db.conn.commit()

        query1 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query1)
        result1 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result1:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

        query2 = "select A.학번, A.이름, A.이메일, B.학과, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where A.학번 = ?"
        db.cursor.execute(query2, (id,))
        result2 = db.cursor.fetchone()

        r_id.config(state="normal")
        r_id.delete(0, tk.END)
        r_id.insert(0, result2[0])
        r_id.config(state="disabled")
        r_name.config(state="normal")
        r_name.delete(0, tk.END)
        r_name.insert(0, result2[1])
        r_name.config(state="disabled")

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.close()