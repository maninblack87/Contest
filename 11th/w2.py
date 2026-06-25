import tkinter as tk
import json

from routes import router
from config import CURRENT_USER
from events import auth

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

    fr1 = tk.Frame(main)
    fr1.pack(side="left")
    lb1 = tk.Label(fr1, text=f"이름: {current_user["name"]}")
    lb1.pack()
    lb2 = tk.Label(fr1, text=f"사번: {current_user["id"]}")
    lb2.pack()
    lb3 = tk.Label(fr1, text=f"권한: {current_user["role"]}")
    lb3.pack()

    line1 = tk.Frame(main, bg="black", width=1)
    line1.pack(side="left", padx=20)

    fr2 = tk.Frame(main)
    fr2.pack(side="right")
    bt1 = tk.Button(fr2, text="학생관리", command=lambda: router.route_w3(root))
    bt1.pack()
    bt2 = tk.Button(fr2, text="암호변경", command=lambda: router.route_w4(root))
    bt2.pack()
    bt3 = tk.Button(fr2, text="로그아웃", command=lambda: auth.logout(root))
    bt3.pack()
    bt4 = tk.Button(fr2, text="종료", command=root.quit)
    bt4.pack()

    root.mainloop()


if __name__ == "__main__":
    main()