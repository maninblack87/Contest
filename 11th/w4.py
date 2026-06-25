import tkinter as tk
from events import auth
from routes import router

def main():
    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("900x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    def check_entries(*args):
        currpw = en1_var.get()
        newpw = en2_var.get()
        confpw = en3_var.get()
        if len(currpw) < 8 or len(newpw) < 8 or len(confpw) < 8:
            bt1.config(state="disabled")
            return
        if newpw != confpw:
            bt1.config(state="disabled")
            return
        if currpw == newpw:
            bt1.config(state="disabled")
            return
        bt1.config(state="normal")

    en1_var = tk.StringVar()
    en2_var = tk.StringVar()
    en3_var = tk.StringVar()
    en1_var.trace_add("write", check_entries)
    en2_var.trace_add("write", check_entries)
    en3_var.trace_add("write", check_entries)

    f1 = tk.Frame(main)
    f1.pack()
    lb1 = tk.Label(f1, text="현재 암호")
    lb1.pack(side="left")
    en1 = tk.Entry(f1, width=15, show="*")
    en1.pack(side="left")
    
    f2 = tk.Frame(main)
    f2.pack()
    lb2 = tk.Label(f2, text="새 암호")
    lb2.pack(side="left")
    en2 = tk.Entry(f2, width=15, show="*")
    en2.pack(side="left")

    f3 = tk.Frame(main)
    f3.pack()
    lb3 = tk.Label(f3, text="새암호확인")
    lb3.pack(side="left")
    en3 = tk.Entry(f3, width=15, show="*")
    en3.pack(side="left")

    f4 = tk.Frame(main)
    f4.pack()
    bt1 = tk.Button(f4, text="저장", state="disabled", command=lambda: auth.change_pw(en1, en2, en3, root))
    bt1.pack(side="left")
    bt2 = tk.Button(f4, text="취소", command=lambda: router.route_w2(root))
    bt2.pack(side="left")

    root.mainloop()