# w2.py
import tkinter as tk
import json

from routes import router
from auth import logout

def main():

    # CurrentUser.json에서 현재 사용자 정보 불러오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 기본 창
    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("400x250")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 메인 프레임
    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(fill="both")

    # 현재 사용자 정보
    frame1 = tk.Frame(main_frame)
    frame1.pack(side="left", fill="both")
    # 1. 이름
    label1 = tk.Label(frame1, text=f"이름 : {current_user['name']}", font="Gothic 16")
    label1.pack(side="top")
    # 2. 사번
    label2 = tk.Label(frame1, text=f"사번 : {current_user['id']}", font="Gothic 16")
    label2.pack(side="top")
    # 3. 권한
    label3 = tk.Label(frame1, text=f"권한 : {current_user['role']}", font="Gothic 16")
    label3.pack(side="top")

    # 구분선(중앙)
    divide_line = tk.Frame(main_frame, width=1, bg="black")
    divide_line.pack(side="left", fill="y")

    # 버튼 셋
    frame2 = tk.Frame(main_frame)
    frame2.pack(side="left", fill="both")
    # 1. 학생관리(w3.py으로 이동)
    button1 = tk.Button(frame2, text="학생관리", command=lambda: router.run_w3(root))
    button1.pack(side="top")
    # 2. 암호변경(w4.py으로 이동)
    button2 = tk.Button(frame2, text="암호변경", command=lambda: router.run_w4(root))
    button2.pack(side="top")
    # 3. 로그아웃
    button3 = tk.Button(frame2, text="로그아웃", command=lambda: logout.logout(root))
    button3.pack(side="top")
    # 4. 종료
    button4 = tk.Button(frame2, text="종료", command=root.quit)
    button4.pack(side="top")

    # 창 활성화
    root.mainloop()


if __name__ == "__main__":
    main()