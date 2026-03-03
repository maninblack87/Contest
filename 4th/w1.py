# w1.py
# 로그인 창
import tkinter as tk

def main():

    # 내장 함수 - 사번과 암호의 입력창이 8자씩 입력되면 -> 로그인 버튼 활성화
    def check_entries(*args):
        id = entry1_var.get()
        pw = entry2_var.get()
        if len(id) == 8 and len(pw) == 8:
            btn_login.config(state="normal")
        else:
            btn_login.config(state="disabled")

    # 내장 함수 - 사번 입력은 숫자만!
    def check_only_numeric(char):
        return char.isdigit()
        

    # 기본 창
    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")
    # 유효성 검사 함수 등록(순서 주의!)
    vcmd = (root.register(check_only_numeric), '%S')

    # 메인 프레임
    main = tk.Frame(root, bg="#ffaaaa")
    main.pack(fill="both", padx=20, pady=20)

    # 위젯 - 사번
    frame1 = tk.Frame(main)
    frame1.pack(fill="both")
    label1 = tk.Label(frame1, text="사번")
    label1.pack(side="left")
    entry1_var = tk.StringVar()
    entry1_var.trace_add("write", check_entries)
    entry1 = tk.Entry(frame1, textvariable=entry1_var, validate='key', validatecommand=vcmd)
    entry1.pack(side="left")

    # 위젯 - 암호
    frame2 = tk.Frame(main)
    frame2.pack(fill="both")
    label2 = tk.Label(frame2, text="암호")
    label2.pack(side="left")
    entry2_var = tk.StringVar()
    entry2_var.trace_add("write", check_entries)
    entry2 = tk.Entry(frame2, textvariable=entry2_var, validate='key', validatecommand=vcmd)
    entry2.pack(side="left")

    # 버튼
    frame3 = tk.Frame(main)
    frame3.pack(fill="both")
    btn_quit = tk.Button(frame3, text="종료", command=root.quit)
    btn_quit.pack(side="right")
    btn_login = tk.Button(frame3, text="로그인")    # 여기부터
    btn_login.pack(side="right")

    # 창 활성화
    root.mainloop()