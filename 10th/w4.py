import tkinter as tk

from routes import router

def main():
    root = tk.Tk()
    root.title("암호 변경")
    root.geometry("300x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    def check_entries(*args):
        cur_pw = entry1.get()
        new_pw = entry2.get()
        conf_pw = entry3.get()
        if len(cur_pw) < 8 or len(cur_pw) < 8 or len(cur_pw) < 8:
            button1.config(state="disabled")
            return
        if new_pw != conf_pw:
            button1.config(state="disabled")
            return
        if cur_pw == new_pw:
            button1.config(state="disabled")
            return
        button1.config(state="normal")
        return
    
    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    frame1 = tk.Frame(main)
    frame1.pack(side="top")
    label1 = tk.Label(frame1, text="현재 암호")
    label1.pack(side="left", padx=5)
    entry1_var = tk.StringVar()
    entry1_var.trace_add('write', check_entries)
    entry1 = tk.Entry(frame1, width=20, show="*", textvariable=entry1_var)
    entry1.pack(side="left", padx=5)

    frame2 = tk.Frame(main)
    frame2.pack(side="top")
    label2 = tk.Label(frame2, text="새 암호")
    label2.pack(side="left", padx=5)
    entry2_var = tk.StringVar()
    entry2_var.trace_add('write', check_entries)
    entry2 = tk.Entry(frame2, width=20, show="*", textvariable=entry2_var)
    entry2.pack(side="left", padx=5)

    frame3 = tk.Frame(main)
    frame3.pack(side="top")
    label3 = tk.Label(frame3, text="새 암호 확인")
    label3.pack(side="left", padx=5)
    entry3_var = tk.StringVar()
    entry3_var.trace_add('write', check_entries)
    entry3 = tk.Entry(frame3, width=20, show="*", textvariable=entry3_var)
    entry3.pack(side="left", padx=5)

    frame4 = tk.Frame(main)
    frame4.pack(side="top", anchor="e")
    button1 = tk.Button(frame4, text="저장", state="disabled", command=None)
    button1.pack(side="left", padx=5)
    button2 = tk.Button(frame4, text="취소", command=lambda: router.route_w1(root))
    button2.pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()