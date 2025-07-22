import tkinter as tk
from tkinter import ttk

import Connect

db_connection = Connect.connect_to_mysql()
cursor = db_connection.cursor()

root = tk.Tk()
root.title("학생관리")
root.geometry("800x500+150+150")
root.resizable(False, False)
root.option_add("*Font", "Gothic 12")

# 프레임1 : 검색부
query = "select 명칭 from 학과정보"
cursor.execute(query)
majors = [m[0] for m in cursor.fetchall()]
majors.insert(0, "전체")
# >>
frame1 = tk.Frame(root, height=50)
frame1.pack(side="top", fill="both", padx=20, pady=5)
label1 = tk.Label(frame1, text="학과", width=5, height=1)
label1.pack(side="left")
combo1 = ttk.Combobox(frame1, values=majors, state="readonly", width=15)
combo1.pack(side="left", padx=10)
combo1.current(0)
label2 = tk.Label(frame1, text="학번", width=5, height=1)
label2.pack(side="left")
entry2 = tk.Entry(frame1, width=10)
entry2.pack(side="left", padx=10)
label3 = tk.Label(frame1, text="이름", width=5, height=1)
label3.pack(side="left")
entry3 = tk.Entry(frame1, width=10)
entry3.pack(side="left", padx=10)
button1 = tk.Button(frame1, text="검색", width=10)
button1.pack(side="left", padx=10)

# 구분선
seperating1 = tk.Frame(root, height=2, bg="gray")
seperating1.pack(side="top", fill="x")


# 프레임2 : 테이블(트리뷰) 부분
frame2 = tk.Frame(root, width=500)
frame2.pack(side="left", fill="both", padx=20, pady=10)
# 테이블
tree = ttk.Treeview(frame2, columns=("이름", "학번", "학과", "상태"), show="headings")
tree.heading("이름", text="이름")
tree.heading("학번", text="학번")
tree.heading("학과", text="학과")
tree.heading("상태", text="상태")
# 테이블 크기
tree.column("이름", width=100)
tree.column("학번", width=100)
tree.column("학과", width=100)
tree.column("상태", width=60)
# 스크롤바
scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
# 테이블 배치
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 프레임3 : 입력부
frame3 = tk.Frame(root, width=500)
frame3.pack(side="right", fill="both")

root.mainloop()