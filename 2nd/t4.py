import tkinter as tk

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
entry1 = tk.Entry(frame1, width=30, show="*")
entry1.pack(side="left")

# 프레임2 : 새 암호
frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10, pady=10)
label2 = tk.Label(frame2, text="새 암호", width=10)
label2.pack(side="left", padx=10, anchor="e")
entry2 = tk.Entry(frame2, width=30, show="*")
entry2.pack(side="left")

# 프레임3 : 새 암호 확인
frame3 = tk.Frame(root)
frame3.pack(fill="x", padx=10, pady=10)
label3 = tk.Label(frame3, text="새 암호 확인", width=10)
label3.pack(side="left", padx=10, anchor="e")
entry3 = tk.Entry(frame3, width=30, show="*")
entry3.pack(side="left")

# 프레임4 : 버튼 {저장, 취소}
frame4 = tk.Frame(root)
frame4.pack(side="right", padx=10, pady=10)
button1 = tk.Button(frame4, text="저장", state="disabled")
button1.pack(side="left", ipadx=10, padx=10)
button2 = tk.Button(frame4, text="취소")
button2.pack(side="left", ipadx=10, padx=10)

root.mainloop()