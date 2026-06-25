import tkinter as tk
import json

from routes import router
from auth.user_manager import logout
from config import CURRENT_USER

def main():
    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    with open (CURRENT_USER, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    main = tk.Frame(root, padx=10, pady=10)
    main.pack()

    frame1 = tk.Frame(main)
    frame1.pack(side="left")
    label1 = tk.Label(frame1, text=f"이름 : {current_user['name']}")
    label1.pack(side="top", anchor="w")
    label2 = tk.Label(frame1, text=f"사번 : {current_user['id']}")
    label2.pack(side="top", anchor="w")
    label3 = tk.Label(frame1, text=f"권한 : {current_user['role']}")
    label3.pack(side="top", anchor="w")

    line1 = tk.Frame(main, width=1, bg="black")
    line1.pack(side="left", fill="y")

    frame2 = tk.Frame(main)
    frame2.pack(side="right")
    button1 = tk.Button(frame2, text="학생 관리", command=lambda: router.route_w3(root))
    button1.pack(side="top", pady=5)
    button2 = tk.Button(frame2, text="암호 변경", command=lambda: router.route_w4(root))
    button2.pack(side="top", pady=5)
    button3 = tk.Button(frame2, text="로그아웃", command=lambda: logout(root))
    button3.pack(side="top", pady=5)
    button4 = tk.Button(frame2, text="종료", command=root.quit)
    button4.pack(side="top", pady=5)            

    root.mainloop()


if __name__ == "__main__":
    main()