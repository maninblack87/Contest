# t4.py
import tkinter as tk
from tkinter import messagebox

import Event
import Router
import Query

root = tk.Tk()
root.title("암호 변경")
root.geometry("400x200")
root.resizable(False, False)
root.option_add("*Font", "Gothic 12")

# 프레임1 : 현재 암호
frame1 = tk.Frame(root)
frame1.pack(fill="x", padx=10, pady=10)
label1 = tk.Label(frame1, text="현재 암호", width=10)
label1.pack(side="left", padx=10, anchor="e")
var1 = tk.StringVar()
entry1 = tk.Entry(frame1, width=30, textvariable=var1, show="*")
entry1.pack(side="left")

# 프레임2 : 새 암호
frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10, pady=10)
label2 = tk.Label(frame2, text="새 암호", width=10)
label2.pack(side="left", padx=10, anchor="e")
var2 = tk.StringVar()
entry2 = tk.Entry(frame2, width=30, textvariable=var2, show="*")
entry2.pack(side="left")

# 프레임3 : 새 암호 확인
frame3 = tk.Frame(root)
frame3.pack(fill="x", padx=10, pady=10)
label3 = tk.Label(frame3, text="새 암호 확인", width=10)
label3.pack(side="left", padx=10, anchor="e")
var3 = tk.StringVar()
entry3 = tk.Entry(frame3, width=30, textvariable=var3, show="*")
entry3.pack(side="left")

# 프레임4 : 버튼 {저장, 취소}
frame4 = tk.Frame(root)
frame4.pack(side="right", padx=10, pady=10)
button1 = tk.Button(frame4, text="저장", state="disabled", command=lambda: on_change_password())
button1.pack(side="left", ipadx=10, padx=10)
button2 = tk.Button(frame4, text="취소", command=lambda: Router.run_t2(root))
button2.pack(side="left", ipadx=10, padx=10)

# 실시간 이벤트 처리
# 모든 입력창(Entry)의 상태 및 조건에 따라, 저장 버튼을 활성화 시키는 함수 호출
def trace_callback(*args):
    Event.check_allowed_change_password(var1.get(), var2.get(), var3.get(), button1)
var1.trace_add("write", trace_callback)
var2.trace_add("write", trace_callback)
var3.trace_add("write", trace_callback)

# 내부 함수 : 암호변경 중 GUI조작
def on_change_password():
    result = Query.change_password(
        var1.get(), var2.get(), var3.get()
    )
    if result == "failed_check1":
        entry1.focus_set()
        entry1.select_range(0, tk.END)
        messagebox.showerror("인증 실패", "현재 비밀번호가 다릅니다")
    elif result == "failed_check2":
        entry3.focus_set()
        messagebox.showerror("불일치", "새 비밀번호가 일치하지 않습니다")
    elif result == "failed_check3":
        entry2.focus_set()
        messagebox.showerror("비밀번호 오류", "기존 비밀번호와 다르게 설정해주세요")
    elif result == "success":
        messagebox.showinfo("성공", "암호 변경 완료")
        Router.run_t2(root)

root.mainloop()