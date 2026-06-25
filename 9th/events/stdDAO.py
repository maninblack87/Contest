import tkinter as tk
from tkinter import ttk, messagebox
import json

from config import DB_FILE, CURRENT_USER
from db.DBconn import DBconn

def onclick_add(
    t_major:ttk.Combobox, 
    t_id:tk.Entry, 
    t_name:tk.Entry, 
    r_id:tk.Entry, 
    r_name:tk.Entry, 
    r_email:tk.Entry, 
    r_major:ttk.Combobox, 
    r_state:ttk.Combobox, 
    tree:ttk.Treeview, 
    btn_del:tk.Button
):
    
    print("onclick_add 시작")
    t_major.current(0)
    t_id.delete(0, tk.END)
    t_name.delete(0, tk.END)

    print("테스트1")
    r_id.config(state="normal")
    r_id.delete(0, tk.END)
    r_name.config(state="normal")
    r_name.delete(0, tk.END)
    r_email.config(state="normal")
    r_email.delete(0, tk.END)
    r_major.config(state="readonly")
    r_major.current(0)
    r_state.config(state="readonly")
    r_state.current(0)
    print("테스트2")
    tree.focus("")
    tree.selection_remove(tree.selection())
    btn_del.config(state="disabled")
    print("onclick_add 종료")


def onclick_save(
    tree:ttk.Treeview, 
    r_id:tk.Entry, 
    r_name:tk.Entry, 
    r_email:tk.Entry, 
    r_major:ttk.Combobox, 
    r_state:ttk.Combobox
):
    node = tree.focus()     # 수정/추가 판단 여부1 : 좌측 목록 데이터 선택여부
    id = r_id.get()
    name = r_name.get()
    email = r_email.get()
    major = r_major.get()
    state = r_state.get()
    print("onclick_save 시작")

    db = DBconn(DB_FILE)
    db.connect()
    print("테스트1 : 데이터베이스 연결")

    if len(id) != 5 and not id.isdigit():
        messagebox.showerror("비 정상적인 값", "학번은 5자리의 숫자")
        return
    if len(name) < 2:
        messagebox.showerror("비 정상적인 값", "이름은 2글자 이상")
        return
    if len(email) < 8:
        messagebox.showerror("비 정상적인 값", "이메일은 8글자 이상")
        return
    if major == "선택":
        messagebox.showerror("비 정상적인 값", "학과를 올바르게 선택해주세요")
        return

    print("테스트2")
    
    db = DBconn(DB_FILE)
    db.connect()
    print("테스트3")

    try:
        db_majors = []
        query1 = "select 명칭 from 학과정보"
        db.cursor.execute(query1)
        result1 = db.cursor.fetchall()
        for r in result1:
            db_majors.append(r[0])
        if major not in db_majors:
            messagebox.showerror("비 정상적인 값", "학과는 데이터베이스 학과 목록 중 하나의 값")
            return
        print("테스트4")

        # 추가/수정될 학과코드 미리 생성
        query4 = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query4, (major,))
        major_code = db.cursor.fetchone()[0]

        if node:
            # 수정
            query1 = "select A.이메일, B.명칭, A.상태 from 학생정보 A join 학과정보 B where A.학번 = ?"
            db.cursor.execute(query1, (id,))
            result1 = db.cursor.fetchone()
            db_email = result1[0]
            db_major = result1[1]
            db_state = result1[2]
            print("수정 테스트1")

            if email == db_email and major == db_major and state == db_state:
                messagebox.showerror("수정 오류", "수정할 부분이 없습니다")
                return
            print("수정 테스트2")
            
            if state not in ["재학", "졸업", "휴학", "퇴학"]:
                messagebox.showerror("비 정상적인 값", "상태는 재학, 졸업, 휴학, 퇴학 중 하나이어야 함")
                return
            print("수정 테스트3")
            
            # 수정 작업
            update_query = "update 학생정보 set 이메일 = ?, 학과 = ?, 상태 = ? where 학번 = ?"
            db.cursor.execute(update_query, (email, major_code, state, id,))
            db.conn.commit()
            print("수정 테스트4(종료)")

        else:
            # 추가
            query2 = "select * from 학생정보 where 학번 = ?"
            db.cursor.execute(query2, (id,))
            result2 = db.cursor.fetchone()
            if result2:
                messagebox.showerror("비 정상적인 값", "기존 학번 데이터와 중복 금지")
                return
            print("추가 테스트1")
            
            if state != "재학":
                messagebox.showerror("비 정상적인 값", "상태는 재학으로 되어야 함")
                return
            print("추가 테스트2")
            
            # 추가 작업
            insert_query = "insert into 학생정보(학번, 이름, 이메일, 학과, 상태) values (?, ?, ?, ?, ?)"
            db.cursor.execute(insert_query, (id, name, email, major_code, state,))
            db.conn.commit()
            print("추가 테스트3(종료)")

        # 좌측 목록 갱신
        query3 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query3)
        result3 = db.cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for r in result3:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))
        print("onclick_save 종료")


    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.close()


    def onclick_delete(tree:ttk.Treeview):
        node = tree.focus()
        if not node:
            return
        values = tree.item(node, 'values')
        if not values or len(values) != 4:
            return
        
        
def onclick_delete(tree:ttk.Treeview, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox, btn_del:tk.Button):
    id = r_id.get()
    node = tree.focus()

    db = DBconn(DB_FILE)
    db.connect()

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    if current_user["role"] != "admin":
        messagebox.showerror("권한 오류", "admin 권한을 가진자만이 삭제를 수행할 수 있습니다")
        return
    
    try:
        delete_query = "delete from 학생정보 where 학번 = ?"
        db.cursor.execute(delete_query, (id,))
        db.conn.commit()

        for i in tree.get_children():
            tree.delete(i)
        query1 = "select A.이름, A.학번, B.명칭, A.상태 from 학생정보 A join 학과정보 B on A.학과 = B.학과코드"
        db.cursor.execute(query1)
        result1 = db.cursor.fetchall()
        for r in result1:
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

        r_id.config(state="normal")
        r_id.delete(0, tk.END)
        r_id.config(state="disabled")
        r_name.config(state="normal")
        r_name.delete(0, tk.END)
        r_name.config(state="disabled")
        r_email.delete(0, tk.END)
        r_major.current(0)
        r_state.current(0)

        btn_del.config(state="disabled")

    except Exception as e:
        messagebox.showerror("알 수 없는 오류", f"알 수 없는 오류 : {e}")
        return
    
    finally:
        db.close()
    