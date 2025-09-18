# events.onClickSave.py
import tkinter as tk
from tkinter import ttk, messagebox

from query import addStudent

def on_click_save(id:tk.Entry, name:tk.Entry, email:tk.Entry, major:ttk.Combobox, state:ttk.Combobox):
    """
    저장 버튼을 클릭하면 동작하는 함수
    """
    id_val = id.get()
    name_val = name.get()
    email_val = email.get()
    major_val = major.get()
    state_val = state.get()

    # 추가 or 수정 여부 확인
    # >> 추가일 경우, 학번/이름/이메일 입력창이 활성화된다
    if id.cget("state") == "normal":

        # 추가 쿼리를 수행하기전 해당 조건이 모두 만족해야 한다
        # 1. 학번은 5자리 숫자로만 허용
        if len(id_val) != 5:
            messagebox("오류발생", "비정상적인 값 : 학번은 5자리 숫자만 허용")
            return

        # 2. 이름은 최소 2글자 이상
        if len(name_val) < 2:
            messagebox("오류발생", "비정상적인 값 : 이름은 2글자 이상만 허용")
            return

        # 3. 이메일은 최소 8글자 이상
        if len(email_val) < 8:
            messagebox("오류발생", "비정상적인 값 : 이메일은 8글자 이상만 허용")
            return
            
        # 4. 학과는 데이터베이스 학과목록 중 하나의 값이 선택되어야 한다
        query = "select 명칭 from 학과정보"
        if not major_val in []

        # 5. 상태는 재학으로만 선택 되어있어야 한다

        # 추가 쿼리를 수행한다
        addStudent(id_val, name_val, email_val, major_val, state_val)

        # 추가 성공 메세지
        messagebox.showinfo("학생 추가 성공", "학생 추가에 성공했습니다")

        # 추가 성공 후


    else:
        # 수정 쿼리를 수행한다
        print("수정 쿼리 수행문을 작성한다")

    # 1. 추가일 경우
    # 1-1. 추가 쿼리
    # 1-2. 추가 성공 후 메세지
    # 1-3. 추가 성공 후 처리
    # >> 학번, 이름, 이메일 비활성화

    # 2. 수정일 경우