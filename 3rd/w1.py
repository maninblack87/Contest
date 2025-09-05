# w1.py
# 로그인 창
import tkinter as tk

from auth import Login

def main():

    # 내장 함수
    # 1. 로그인 입력창이 모두 8자씩 입력되면 로그인 버튼이 활성화되는 함수
    def check_entries(*args):
        id = entry1_var.get()
        pw = entry2_var.get()
        if len(id) == 8 and len(pw) == 8:
            btn_login.config(state="normal")
        else:
            btn_login.config(state="disabled")

    # 2. 사번 입력시 숫자만 입력할 수 있게하는 함수
    def check_only_numeric(char):
        return char.isdigit()

    
    # 루트 윈도우 생성
    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 유효성 검사 함수 등록
    vcmd = (root.register(check_only_numeric), '%S')

    # 메인 프레임 생성
    main = tk.Frame(root)
    main.pack(fill="both", padx=20, pady=20)

    # 위젯 구성
    # 1. 사번
    frame1 = tk.Frame(main, pady=10)
    frame1.pack(side="top", fill="both")
    label1 = tk.Label(frame1, text="사번", width=6, anchor="e", padx=10)
    label1.pack(side="left")
    entry1_var = tk.StringVar()
    entry1_var.trace_add("write", check_entries)
    entry1 = tk.Entry(frame1, width=32, textvariable=entry1_var, validate='key', validatecommand=vcmd)
    entry1.pack(side="left")

    # 2. 암호
    frame2 = tk.Frame(main, pady=10)
    frame2.pack(side="top", fill="both")
    label2 = tk.Label(frame2, text="암호", width=6, anchor="e", padx=10)
    label2.pack(side="left")
    entry2_var = tk.StringVar()
    entry2_var.trace_add("write", check_entries)
    entry2 = tk.Entry(frame2, width=32, textvariable=entry2_var, show="*")
    entry2.pack(side="left")

    # 3. 버튼
    frame3 = tk.Frame(main, pady=10, padx=10)
    frame3.pack(side="top", fill="both")
    btn_quit = tk.Button(frame3, text="종료", width=8, command=root.quit)
    btn_quit.pack(side="right", padx=10)
    btn_login = tk.Button(frame3, text="로그인", width=8, command=lambda: Login.login(entry1, entry2, root), state="disabled")
    btn_login.pack(side="right", padx=10)
    
    # 루트 윈도우를 활성화
    root.mainloop()


if __name__ == "__main__":
    main()