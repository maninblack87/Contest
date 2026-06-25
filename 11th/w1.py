import tkinter as tk
from events import auth

def main():
    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("300x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    def check_only_numeric(char:str):
        return char.isdigit()
    vcmd = (root.register(check_only_numeric), "%S")

    def check_entries(*args):
        id = en1_var.get()
        pw = en2_var.get()
        if (len(id) > 0) and (len(pw) > 0):
            bt1.config(state="normal")
        else:
            bt1.config(state="disabled")

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    en1_var = tk.StringVar()
    en2_var = tk.StringVar()
    en1_var.trace_add("write", check_entries)
    en2_var.trace_add("write", check_entries)

    fr1 = tk.Frame(main)
    fr1.pack()
    lb1 = tk.Label(fr1, text="사번")
    lb1.pack(side="left")
    en1 = tk.Entry(fr1, width=20, textvariable=en1_var, validate="key", validatecommand=vcmd)
    en1.pack(side="left")

    fr2 = tk.Frame(main)
    fr2.pack()
    lb2 = tk.Label(fr2, text="암호")
    lb2.pack(side="left")
    en2 = tk.Entry(fr2, width=20, textvariable=en2_var, validate="key", validatecommand=vcmd, show="*")
    en2.pack(side="left")

    fr3 = tk.Frame(main)
    fr3.pack(anchor="e")
    bt1 = tk.Button(main, text="로그인", command=lambda: auth.login(en1, en2, root), state="disabled")
    bt1.pack(side="left")
    bt2 = tk.Button(main, text="종료", command=root.quit)
    bt2.pack(side="left")

    root.mainloop()