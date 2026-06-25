import tkinter as tk
from tkinter import ttk, messagebox
import json

from config import DB_FILE, CURRENT_USER
from db.dbconn import DBconn

def onclick_add(t_major:ttk.Combobox, t_id:tk.Entry, t_name:tk.Entry, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, tree:ttk.Treeview):

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] != "admin":
        messagebox.showerror("잘못된 권한의 접근", "admin 권한의 업무사용자만 실행가능 합니다.")
        return

    t_major.config(state="readonly")
    t_major.current(0)
    t_id.config(state="normal")
    t_id.delete(0, tk.END)
    t_name.config(state="normal")
    t_name.delete(0, tk.END)

    r_id.config(state="normal")
    r_id.delete(0, tk.END)
    r_name.config(state="normal")
    r_name.delete(0, tk.END)
    r_email.config(state="normal")
    r_email.delete(0, tk.END)
    r_major.config(state="readonly")
    r_major.current(0)
    r_state.config(state="readonly")
    r_state.current(0)  # 재학

    # 선택된 노드의 포커스 해제 / 셀렉션 제거
    tree.focus("")
    tree.selection_remove(tree.selection())


def onclick_save(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()

    # 현재 사용자 정보 가져오기
    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 데이터베이스 연결
    db = DBconn(DB_FILE)
    db.connect()

    if current_user["role"] != "admin":
        messagebox.showerror("잘못된 권한의 접근", "admin 권한의 업무사용자만 실행가능 합니다.")
        return
    
    # 데이터베이스가 필요 없는 조건
    if len(id) != 5 or not id.isdigit():
        messagebox.showerror("비정상적인 값", "학번은 5개 숫자이어야 함")
        return
    if len(name) < 2:
        messagebox.showerror("비정상적인 값", "이름은 2글자 이상이어야 함")
        return
    if len(email) < 8:
        messagebox.showerror("비정상적인 값", "이메일은 8글자 이상이어야 함")
        return
    
    # 선택된 항목
    node = tree.focus()

    try:
        query2 = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query2, (major,))
        result2 = db.cursor.fetchone()
        major_code = result2[0]
        print(f"테스트1 result2 = {result2[0]}")

        db_majors = []
        query1 = "select 명칭 from 학과정보"
        db.cursor.execute(query1)
        result1 = db.cursor.fetchall()
        print(f"테스트2 result1 = {result1}")
        for r in result1:
            db_majors.append(r[0])
        print(f"테스트3 db_majors = {db_majors}")
        if major not in db_majors:
            messagebox.showerror("비정상적인 값", "데이터베이스에 포함된 학과 외에 금지")
            return
        
        if not node:
            # 추가
            print("테스트3.5")
            print(f"테스트3.6 : id = {id}")
            query3 = "select * from 학생정보 where 학번 = ?"
            db.cursor.execute(query3, (id,))
            result3 = db.cursor.fetchone()
            print(f"테스트4 result3 = {result3}")
            if result3:
                messagebox.showerror("비정상적인 값", "기존 학번 데이터와 중복 금지")
                return
            print("테스트5")

            if state != "재학":
                messagebox.showerror("비정상적인 값", "추가시 상태는 반드시 재학이어야 함")
                return
            print("테스트6")
            
            insert_query = "insert into 학생정보 (학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"
            db.cursor.execute(insert_query, (id, name, email, major_code, state,))
            db.conn.commit()
    
        else:
            print(f"node : {node}")
            # 수정
            print("테스트3.5")
            query4 = "select A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드 where 학번 = ?"
            db.cursor.execute(query4, (id,))
            result4 = db.cursor.fetchone()
            db_email = result4[0]
            db_major = result4[1]
            db_state = result4[2]
            if email == db_email and major == db_major and state == db_state:
                messagebox.showerror("수정 취소", "수정할 부분이 없습니다")
                return

            update_query = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ? where 학번 = ?"
            db.cursor.execute(update_query, (email, major_code, state, id,))
            db.conn.commit()

        query5 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query5)
        result5 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result5:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.conn.commit()

    
def onclick_delete(r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, tree:ttk.Treeview, btn_del:tk.Button):
    id = r_id.get()

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] != "admin":
        messagebox.showerror("잘못된 권한의 접근", "admin 권한의 업무사용자만 실행가능 합니다.")
        return
    
    try:
        delete_query = "delete from 학생정보 where 학번 = ?"
        db.cursor.execute(delete_query, (id,))
        db.conn.commit()

        query1 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query1)
        result1 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result1:
            tree.insert("", "end", values = (r[0], r[1], r[2], r[3]))

        r_id.config(state="normal")
        r_id.delete(0, tk.END)
        r_id.config(state="disabled")
        r_name.config(state="normal")
        r_name.delete(0, tk.END)
        r_name.config(state="disabled")
        r_email.config(state="normal")
        r_email.delete(0, tk.END)
        r_major.config(state="normal")
        r_major.delete(0, tk.END)
        r_state.config(state="normal")
        r_state.delete(0, tk.END)

        btn_del.config(state="disabled")

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.close()