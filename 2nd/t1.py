import tkinter as tk
from tkinter import messagebox

from Login import login

# 로그인 버튼의 활성화 조건이 충족하는지 체크하고 활성화/비활성화 시키는 함수
def check_entries(*args):
    id_text = entry1_var.get()
    pw_text = entry2_var.get()
    if len(id_text) == 8 and len(pw_text) == 8:
        button1.config(state="normal")
    else:
        button1.config(state="disabled")

# 숫자만 입력을 허용시키는 함수
def only_numeric(char):
    return char.isdigit()

# 메인 창 생성
root = tk.Tk()
root.title("학생관리프로그램 로그인")
root.geometry("400x150")
root.resizable(False, False)
root.option_add("*Font", "Gothic 12")

vcmd = (root.register(only_numeric), '%S')  # vcmd = validate command

# 사번 프레임
frame1 = tk.Frame(root, padx=30, pady=10)
frame1.pack(side="top", fill="x")
label1 = tk.Label(frame1, text="사번", width=5)
label1.pack(side="left")
# 사번 프레임 > 엔트리
entry1_var = tk.StringVar()
entry1_var.trace_add("write", check_entries)
entry1 = tk.Entry(frame1, textvariable=entry1_var, validate='key', validatecommand=vcmd, width=35)
entry1.pack(side="left")

# 암호 프레임
frame2 = tk.Frame(root, padx=30, pady=10)
frame2.pack(side="top", fill="x")
label2 = tk.Label(frame2, text="암호", width=5)
label2.pack(side="left")
# 사번 프레임 > 엔트리
entry2_var = tk.StringVar()
entry2_var.trace_add("write", check_entries)
entry2 = tk.Entry(frame2, textvariable=entry2_var, validate='key', validatecommand=vcmd, width=35, show="*")
entry2.pack(side="left")

# 버튼 프레임
frame3 = tk.Frame(root, padx=30, pady=10)
frame3.pack(side="right", fill="x")
button1 = tk.Button(frame3, text="로그인", state="disabled", width=5, height=1, command=lambda: login(entry1.get(), entry2.get(), root))
button1.pack(side="left", padx=10, ipadx=2, ipady=1)
button2 = tk.Button(frame3, text="종료", width=5, height=1, command=root.quit)
button2.pack(side="left", padx=10, ipadx=2, ipady=1)

root.mainloop()