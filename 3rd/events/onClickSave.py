# events.onClickSave.py
import tkinter as tk
from tkinter import ttk, messagebox

from query import addStudent, modStudent
from sqlite.DBconnection import DBconnection
from config import DB_FILE

def on_click_save(
        tree:ttk.Treeview, 
        id:tk.Entry, 
        name:tk.Entry, 
        email:tk.Entry, 
        major:ttk.Combobox, 
        state:ttk.Combobox
        ):
    """
    저장 버튼을 클릭하면 동작하는 함수
    """
    # 입력 값만 별도로 정의
    id_val = id.get()
    name_val = name.get()
    email_val = email.get()
    major_val = major.get()
    state_val = state.get()

    # 추가 or 수정 여부 확인
    # 추가일 경우(사번 입력창이 활성화되어 있는지 여부로 확인 가능함)
    if id.cget("state") == "normal":

        # 추가 쿼리를 수행하기전 해당 조건이 모두 만족해야 한다
        # 1. 학번은 5자리 숫자로만 허용
        if len(id_val) != 5:
            messagebox.showerror("오류발생", "비정상적인 값 : 학번은 5자리 숫자만 허용")
            return

        # 2. 이름은 최소 2글자 이상
        if len(name_val) < 2:
            messagebox.showerror("오류발생", "비정상적인 값 : 이름은 2글자 이상만 허용")
            return

        # 3. 이메일은 최소 8글자 이상
        if len(email_val) < 8:
            messagebox.showerror("오류발생", "비정상적인 값 : 이메일은 8글자 이상만 허용")
            return
            
        # 4. 학과는 데이터베이스 학과목록 중 하나의 값이 선택되어야 한다
        db = DBconnection(DB_FILE)
        db.connect()
        query = "select 명칭 from 학과정보"
        db.cursor.execute(query)
        db_majors = [row[0] for row in db.cursor.fetchall()]
        db.close()
        if not major_val in db_majors:
            messagebox.showerror("오류발생", "비정상적인 값 : 학과는 데이터베이스 학과목록 중 하나의 값이 선택되어야 한다")
            return

        # 5. 상태는 재학으로만 선택 되어있어야 한다
        if state_val != "재학":
            messagebox.showerror("오류발생", "비정상적인 값 : 상태는 재학으로만 선택 되어있어야 한다")
            return

        # 추가 쿼리를 수행한다
        # >> 하지만 학생정보.학과 칼럼은 학과명(학과정보.명칭)이 아닌 학과코드가 입력되어야 한다
        db = DBconnection(DB_FILE)
        db.connect()
        query = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query, (major_val,))
        major_code = db.cursor.fetchone()
        db.close()
        # >> 추가 쿼리를 수행
        addStudent.add_student(id_val, name_val, email_val, major_code[0], state_val)

        # 추가 성공 메세지
        messagebox.showinfo("학생 추가 성공", "학생 추가에 성공했습니다")

        # 입력창 초기화
        # >> 학번
        id.delete(0, tk.END)
        id.config(state="disabled")
        # >> 이름
        name.delete(0, tk.END)
        name.config(state="disabled")
        # >> 이메일
        email.delete(0, tk.END)
        # >> 학과
        major.current(0)
        # >> 상태
        state.current(0)


    # 수정일 경우
    else:

        # 수정 쿼리를 수행한다
        db = DBconnection(DB_FILE)
        db.connect()
        query = "select 학과코드 from 학과정보 where 명칭 = ?"
        db.cursor.execute(query, (major_val,))
        major_code = db.cursor.fetchone()
        # >> 수정 쿼리를 수행
        modStudent.mod_student(id_val, email_val, major_code[0], state_val)

        # 수정 성공 메세지
        messagebox.showinfo("학생 추가 성공", "학생 수정에 성공했습니다")


    # 추가/수정이 수행 된 후
    # 1. Treeview 목록 갱신

    # >> 1-1. Treeview 초기화
    for item in tree.get_children():
        tree.delete(item)

    # >> 1-2. Treeview 갱신
    db.connect()
    query = """
        select a.이름, a.학번, b.명칭, a.상태
        from 학생정보 a join 학과정보 b
        on a.학과 = b.학과코드
    """
    db.cursor.execute(query)
    rows = db.cursor.fetchall()

    # >> 1-3. Treeview 목록에 표시
    for row in rows:
        tree.insert("", "end", values=row)