# views/viewMain.py
import tkinter as tk
import json

def main():

    # 테스트용 임시 파일 경로
    file_path = "D:/jeon/Contest/4th/CurrentUser.json"

    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("400x300")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    with open(file_path, "r", encoding="utf-8") as f:
        current_user = json.load(f)

    main_frame = tk.Frame(root, bg="#ffffcc", padx=20, pady=20)
    main_frame.pack(side="top", fill="both")

    left_frame = tk.Frame(main_frame, bg="#ffccff")
    left_frame.pack(side="left", fill="both")
    lbl_name = tk.Label(left_frame, text=f"이름 : {current_user["name"]}", width=20, pady=5)
    lbl_name.pack(side="top", fill="x")
    lbl_id = tk.Label(left_frame, text=f"사번 : {current_user["id"]}", width=20, pady=5)
    lbl_id.pack(side="top", fill="x")
    lbl_role = tk.Label(left_frame, text=f"권한 : {current_user["role"]}", width=20, pady=5)
    lbl_role.pack(side="top", fill="x")

    right_frame = tk.Frame(main_frame, bg="#ccffff")
    right_frame.pack(side="right", fill="both")
    btn_students = tk.Button(right_frame, text="학생관리", width=20, pady=5)
    btn_students.pack(side="top", pady=10)
    btn_password = tk.Button(right_frame, text="암호변경", width=20, pady=5)
    btn_password.pack(side="top", pady=10)
    btn_logout = tk.Button(right_frame, text="로그아웃", width=20, pady=5)
    btn_logout.pack(side="top", pady=10)
    btn_quit = tk.Button(right_frame, text="종료", width=20, pady=5)
    btn_quit.pack(side="top", pady=10)


    root.mainloop()


if __name__ == "__main__":
    main()