import tkinter as tk

from routes import router
from auth.user_manager import change_password

def main():

    root = tk.Tk()
    root.title("암호 변경")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    def check_entries(*args):
        curr_pw = entry1.get()
        new_pw = entry2.get()
        conf_pw = entry3.get()

        if len(curr_pw) != 8 or len(new_pw) != 8 or len(conf_pw) != 8:
            button1.config(state="disabled")
            return
        if new_pw != conf_pw:
            button1.config(state="disabled")
            return
        if curr_pw == new_pw:
            button1.config(state="disabled")
            return
        
        button1.config(state="normal")

    def check_only_numeric(char:str):
        return char.isdigit()
    vcmd = (root.register(check_only_numeric), "%S")


    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    frame1 = tk.Frame(main)
    frame1.pack(side="top", pady=5)
    label1 = tk.Label(frame1, text="현재 암호", width=12, anchor="e")
    label1.pack(side="left", padx=2)
    entry1_var = tk.StringVar()
    entry1_var.trace_add("write", check_entries)
    entry1 = tk.Entry(frame1, width=20, show="*", textvariable=entry1_var, validate="key", validatecommand=vcmd)
    entry1.pack(side="left")

    frame2 = tk.Frame(main)
    frame2.pack(side="top", pady=5)
    label2 = tk.Label(frame2, text="새 암호", width=12, anchor="e")
    label2.pack(side="left", padx=2)
    entry2_var = tk.StringVar()
    entry2_var.trace_add("write", check_entries)
    entry2 = tk.Entry(frame2, width=20, show="*", textvariable=entry2_var, validate="key", validatecommand=vcmd)
    entry2.pack(side="left")

    frame3 = tk.Frame(main)
    frame3.pack(side="top", pady=5)
    label3 = tk.Label(frame3, text="새 암호 확인", width=12, anchor="e")
    label3.pack(side="left", padx=2)
    entry3_var = tk.StringVar()
    entry3_var.trace_add("write", check_entries)
    entry3 = tk.Entry(frame3, width=20, show="*", textvariable=entry3_var, validate="key", validatecommand=vcmd)
    entry3.pack(side="left")

    frame4 = tk.Frame(main)
    frame4.pack(side="top", pady=5, anchor="e")
    button1 = tk.Button(frame4, text="저장", state="disabled", command=lambda: change_password(entry1, entry2, entry3, root))
    button1.pack(side="left", padx=5)
    button2 = tk.Button(frame4, text="취소", command=lambda: router.route_w2(root))
    button2.pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()