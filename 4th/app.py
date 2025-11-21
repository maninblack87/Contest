# app.py
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("300x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    main_frame = tk.Frame(root, padx=20, pady=20, bg="#ffffcc")
    main_frame.pack(side="top", fill="both")

    frame1 = tk.Frame(main_frame)
    frame1.pack(side="top", pady=5)
    lbl_id = tk.Label(frame1, text="사번")
    lbl_id.pack(side="left", padx=10)
    ent_id = tk.Entry(frame1, width=20, show="*")
    ent_id.pack(side="left", padx=10)

    frame2 = tk.Frame(main_frame)
    frame2.pack(side="top", pady=5)
    lbl_pw = tk.Label(frame2, text="암호")
    lbl_pw.pack(side="left", padx=10)
    ent_pw = tk.Entry(frame2, width=20, show="*")
    ent_pw.pack(side="left", padx=10)

    frame3 = tk.Frame(main_frame)
    frame3.pack(side="top", pady=5)
    btn_login = tk.Button

    root.mainloop()


if __name__ == "__main__":
    main()