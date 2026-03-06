# w3.py

import tkinter as tk

def main():

    # 기본 창
    root = tk.Tk()
    root.title("학생 관리")
    root.geometry("800x400")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    frame1 = tk.Frame(root, bg="#ffaaaa", width=10, height=10)
    frame1.pack(side="top", fill="both")

    frame2 = tk.Frame(root, bg="#aaffaa")
    frame2.pack(side="left", fill="both")

    frame3 = tk.Frame(root, bg="#aaaaff")
    frame3.pack(side="right", fill="both")

    # 창 활성화
    root.mainloop()


if __name__ == "__main__":
    main()