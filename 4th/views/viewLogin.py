# views/viewLogin.py
import tkinter as tk
from modules import Login

def main():

    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(side="top")

    frame1 = tk.Frame(main_frame)
    frame1.pack(side="top", pady=10)
    lbl_id = tk.Label(frame1, text="사번", width=7)
    lbl_id.pack(side="left")
    ent_id_var = tk.StringVar()
    ent_id = tk.Entry(frame1, width=35, textvariable=ent_id_var, show="*")
    ent_id.pack(side="left")

    frame2 = tk.Frame(main_frame)
    frame2.pack(side="top", pady=10)
    lbl_pw = tk.Label(frame2, text="암호", width=7)
    lbl_pw.pack(side="left")
    ent_pw_var = tk.StringVar()
    ent_pw = tk.Entry(frame2, width=35, textvariable=ent_pw_var, show="*")
    ent_pw.pack(side="left")

    frame3 = tk.Frame(main_frame)
    frame3.pack(side="bottom", fill="x")
    btn_quit = tk.Button(frame3, text="종료", command=root.quit)
    btn_quit.pack(side="right", padx=10)
    btn_login = tk.Button(frame3, text="로그인", command=lambda: Login.login(ent_id_var.get(), ent_pw_var.get(), root))
    btn_login.pack(side="right", padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()