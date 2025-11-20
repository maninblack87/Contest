# views/viewMain.py
import tkinter as tk
import json

def main():

    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("400x250")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    main_frame = tk.Frame(root, bg="#ffffcc", padx=20, pady=20)
    main_frame.pack(side="top", fill="both")

    left_frame = tk.Frame(main_frame, bg="#ffccff")
    left_frame.pack(side="left", fill="both")
    lbl_name = tk.Label(left_frame, text=f"이름 : {current_user["name"]}")
    lbl_name.pack(side="top", fill="x")
    lbl_id = tk.Label(left_frame, text=f"사번 : {current_user["id"]}")
    lbl_id.pack(side="top", fill="x")
    lbl_role = tk.Label(left_frame, text=f"권한 : {current_user["role"]}")
    lbl_role.pack(side="top", fill="x")

    right_frame = tk.Frame(main_frame, bg="#ccffff")
    right_frame.pack(side="right", fill="both")
    


    root.mainloop()


if __name__ == "__main__":
    main()