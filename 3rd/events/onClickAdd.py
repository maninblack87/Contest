# events/onClickAdd.py
import tkinter as tk
from tkinter import ttk

def on_click_add(top_id:tk.Entry, top_name:tk.Entry, top_major:ttk.Combobox, r_id:tk.Entry, r_name:tk.Entry, r_email:tk.Entry, r_major:ttk.Combobox, r_state:ttk.Combobox):
    """
    "추가"버튼을 클릭하면 작동하는 함수
    """

    # 상단의 학번, 이름은 입력 가능한 비어있는 상태로
    top_id.delete(0, tk.END)
    top_name.delete(0, tk.END)

    # 상단의 학과의 값이 '전체학과'로 선택된 상태로
    top_major.current(0)

    # 우측 학번, 이름, 이메일은 입력 가능한 비어있는 상태로
    # >> 학번
    r_id.config(state="normal")
    r_id.delete(0, tk.END)
    # >> 이름
    r_name.config(state="normal")
    r_name.delete(0, tk.END)
    # >> 이메일
    r_email.config(state="normal")
    r_email.delete(0, tk.END)

    # 우측 학과는 선택이 선택된 상태
    r_major.config(state="normal")
    r_major.current(0)

    # 우측 상태는 재학으로 되어있어야 함
    r_state.config(state="normal")
    r_state.current(0)
    