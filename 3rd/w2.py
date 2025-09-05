# w2.py
import tkinter as tk
import json

from routes import Router

def main():

    # CurrentUser.json에서 현재 사용자 정보 불러오기
    with open("CurrentUser.json", "r", encoding="utf-8") as f:
        current_user = json.load(f)

    # 루트 윈도우 생성
    root = tk.Tk()
    root.title("학생관리 프로그램")
    root.geometry("400x250")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 프레임(좌측) 생성
    frame_left = tk.Frame(root, width=200)
    frame_left.pack(side="left", fill="both", padx=10, pady=20)
    # 이름
    label1 = tk.Label(frame_left, text=f"이름 : {current_user['name']}", font="Gothic 16")
    label1.pack(side="top", pady=5, anchor="w")
    # 사번
    label2 = tk.Label(frame_left, text=f"사번 : {current_user['id']}", font="Gothic 16")
    label2.pack(side="top", pady=5, anchor="w")
    # 권한
    label3 = tk.Label(frame_left, text=f"권한 : {current_user['role']}", font="Gothic 16")
    label3.pack(side="top", pady=5, anchor="w")

    # 구분선(중앙)
    divide_line = tk.Frame(root, width=1, bg="black")
    divide_line.pack(side="left", fill="y", pady=20, padx=20)

    # 프레임(우측) 생성
    frame_right = tk.Frame(root, width=150, pady=20, padx=10)
    frame_right.pack(side="right", fill="both")
    # 버튼 부분 : 학생관리, 암호변경, 로그아웃, 종료
    button1 = tk.Button(frame_right, width=24, text="학생 관리", command=lambda: Router.run_w3(root))
    button1.pack(side="top", pady=5, ipady=5)
    button2 = tk.Button(frame_right, width=24, text="암호 변경", command=lambda: Router.run_w4(root))
    button2.pack(side="top", pady=5, ipady=5)
    button3 = tk.Button(frame_right, width=24, text="로그 아웃")
    button3.pack(side="top", pady=5, ipady=5)
    button4 = tk.Button(frame_right, width=24, text="종료", command=root.quit)
    button4.pack(side="top", pady=5, ipady=5)

    root.mainloop()


if __name__ == '__main__':
    main()