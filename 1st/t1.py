import tkinter as tk
from tkinter import messagebox

from Login import login


# 로그인 버튼 활성화 조건 확인 함수
def check_entries(*args):
    id_text = entry1_var.get()
    pw_text = entry2_var.get()
    if len(id_text) == 8 and len(pw_text) == 8:
        button1.config(state="normal")
    else:
        button1.config(state="disabled")


# 메인 창 생성
root = tk.Tk()
root.title("학생관리프로그램 로그인")
root.geometry("400x150")
root.resizable(False, False)

# 메인 창 옵션 추가
root.option_add("*Font", "Gothic 12")

# 그리드 레이아웃을 사용하여 배치
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# 1. 사번
# 사번 레이블
label1 = tk.Label(root, text="사번", width=5)
label1.grid(row=0, column=0, padx=10, pady=5)

# 사번 변수와 엔트리
entry1_var = tk.StringVar()
# 숫자만 입력 허용하는 함수 (입력 문자 char가 숫자인지 검사)
def only_numeric(char):
    return char.isdigit()
# 함수 등록 및 validatecommand 생성
vcmd = (root.register(only_numeric), '%S')  # %S는 입력한 문자 하나
# 값이 바뀔 때마다 check_entries 호출
entry1_var.trace_add("write", check_entries)
# 엔트리 생성
entry1 = tk.Entry(root, textvariable=entry1_var, validate='key', validatecommand=vcmd, width=30)
entry1.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

# 2. 암호
# 암호 레이블
label2 = tk.Label(root, text="암호", width=5)
label2.grid(row=1, column=0, padx=10, pady=5)

# 암호 변수와 엔트리
entry2_var = tk.StringVar()
entry2_var.trace_add("write", check_entries)
entry2 = tk.Entry(root, textvariable=entry2_var, width=30, show="*")  # show="*"으로 암호 마스킹
entry2.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

# 3. 로그인
# 로그인 버튼
button1 = tk.Button(root, text="로그인", state="disabled", command=lambda: login(entry1.get(), entry2.get(), root))
button1.grid(row=2, column=1, padx=10, pady=5)

# 4. 종료
# 종료 버튼
button2 = tk.Button(root, width=8, text="종료", command=root.quit)
button2.grid(row=2, column=2, padx=10, pady=5)

root.mainloop()