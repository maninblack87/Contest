# t1.py
import tkinter as tk

from modules import Login

def main():
    # 루트 위젯
    root = tk.Tk()
    root.title("학생관리 프로그램 로그인")
    root.geometry("400x200")
    root.resizable(False, False)
    root.option_add("*Font", "Gothic 12")

    # 메인 프레임
    main = tk.Frame(root)
    main.pack(fill="both", padx=20, pady=20)

    # 위젯 구성
    # >> 사번(user_id)
    frame1 = tk.Frame(main)
    frame1.pack(side="top", fill="x")
    label1 = tk.Label(frame1, text="사번", width=8, anchor="e")
    label1.pack(side="left", padx=10, pady=10)
    entry1 = tk.Entry(frame1, width=30)
    entry1.pack(side="left", pady=10)
    # >> 암호
    frame2 = tk.Frame(main)
    frame2.pack(side="top", fill="x")
    label2 = tk.Label(frame2, text="암호", width=8, anchor="e")
    label2.pack(side="left", padx=10, pady=10)
    entry2 = tk.Entry(frame2, width=30)
    entry2.pack(side="left", pady=10)
    # >> 버튼
    frame3 = tk.Frame(main)
    frame3.pack(side="bottom", fill="x")
    quit_btn = tk.Button(frame3, text="종료", width=8, command=root.quit)
    quit_btn.pack(side="right", padx=10, pady=10)
    login_btn = tk.Button(frame3, text="로그인", width=8, command=lambda: Login.login(entry1.get(), entry2.get(), root))
    login_btn.pack(side="right", pady=10)

    # 루트 위젯을 GUI로 활성화
    root.mainloop()


# 독립 실행
if __name__ == "__main__":
    main()