import tkinter as tk

from auth.user_manager import login

def main():
    
    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("300x150")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    def check_entries(*args):
        id = entry1.get()
        pw = entry2.get()
        if len(id) == 8 and len(pw) == 8:
            button1.config(state="normal")
        else:
            button1.config(state="disabled")

    def check_only_numeric(char:str):
        return char.isdigit()
    vcmd = (root.register(check_only_numeric), "%S")

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    frame1 = tk.Frame(main)
    frame1.pack(side="top", pady=5)
    label1 = tk.Label(frame1, text="사번")
    label1.pack(side="left")
    entry1_var = tk.StringVar()
    entry1_var.trace_add('write', check_entries)
    entry1 = tk.Entry(frame1, width=20, textvariable=entry1_var, validate="key", validatecommand=vcmd)
    entry1.pack(side="left")

    frame2 = tk.Frame(main)
    frame2.pack(side="top", pady=5)
    label2 = tk.Label(frame2, text="암호")
    label2.pack(side="left")
    entry2_var = tk.StringVar()
    entry2_var.trace_add('write', check_entries)
    entry2 = tk.Entry(frame2, width=20, show="*", textvariable=entry2_var, validate="key", validatecommand=vcmd)
    entry2.pack(side="left")

    frame3 = tk.Frame(main)
    frame3.pack(side="top", anchor="e", pady=5)
    button1 = tk.Button(frame3, text="로그인", state="disabled", command=lambda: login(entry1, entry2, root))
    button1.pack(side="left", padx=5)
    button2 = tk.Button(frame3, text="종료", command=root.quit)
    button2.pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()