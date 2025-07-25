import tkinter as tk
from tkinter import ttk
import json

import Connect
from Query import searchStudentInfo
from Event import on_tree_select

# 데이터베이스 연결 및 (쿼리를 전송할) 커서 생성
db_connection = Connect.connect_to_mysql()
cursor = db_connection.cursor()

# 로그인중인 사용자 정보를 JSON 파일에서 불러오기
with open("CurrentUser.json", "r", encoding="utf-8") as f:
    current_user = json.load(f)

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
button1 = tk.Button(frame1, text="검색", width=10, command= lambda: searchStudentInfo(combo1.get(), entry2.get(), entry3.get(), tree))
button1.pack(side="left", padx=10)

# 구분선
seperating1 = tk.Frame(root, height=2, bg="gray")
seperating1.pack(side="top", fill="x")

# 프레임2 : 테이블(트리뷰) 부분
frame2 = tk.Frame(root, width=500, bg="green")
frame2.pack(side="left", fill="y", padx=20, pady=10)
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
tree.pack(side="left", fill="both")
scrollbar.pack(side="right", fill="y")

# 프레임3 : 입력부
frame3 = tk.Frame(root, width=500)
frame3.pack(side="left", fill="both", padx=10, pady=20)
# >> 프레임3-1
frame3_1 = tk.Frame(frame3, pady=10)
frame3_1.pack(side="top", anchor="w")
# >> >> 학번
label4 = tk.Label(frame3_1, text="학번", width=5)
label4.pack(side="left")
entry4 = tk.Entry(frame3_1, width=12)
entry4.pack(side="left", padx=20)
# >> >> 이름
label5 = tk.Label(frame3_1, text="이름", width=5)
label5.pack(side="left")
entry5 = tk.Entry(frame3_1, width=12)
entry5.pack(side="left")
# >> 프레임3-2
frame3_2 = tk.Frame(frame3, pady=10)
frame3_2.pack(side="top", anchor="w")
# >> >> 이메일
label6 = tk.Label(frame3_2, text="이메일", width=5)
label6.pack(side="left")
entry6 = tk.Entry(frame3_2, width=32)
entry6.pack(side="left")
# >> 프레임3-3
# >> >> 학과 명칭 조회 쿼리
query = "SELECT 명칭 FROM 학과정보"
cursor.execute(query)
majors = [row[0] for row in cursor.fetchall()]
majors.insert(0, "선택")
frame3_3 = tk.Frame(frame3, pady=10)
frame3_3.pack(side="top", anchor="w")
# >> >> 학과
label7 = tk.Label(frame3_3, text="학과", width=5)
label7.pack(side="left")
combo7 = ttk.Combobox(frame3_3, value=majors, state="readonly", width=15)
combo7.pack(side="left")
# >> >> 상태
label8 = tk.Label(frame3_3, text="상태")
label8.pack(side="left")
# >> >> >> 학생 상태 조회 쿼리
status = ["재학", "졸업", "휴학", "퇴학"]
combo8 = ttk.Combobox(frame3_3, values=status, state="readonly", width=8)
combo8.pack(side="left")

# >> 프레임 3-4
frame3_4 = tk.Frame(frame3, pady=10)
frame3_4.pack(side="bottom", anchor="w")
# >> >> 추가 버튼
add_btn = tk.Button(frame3_4, text="추가")
add_btn.pack(side="left")
# >> >> 저장 버튼
save_btn = tk.Button(frame3_4, text="저장")
save_btn.pack(side="left")
# >> >> 삭제 버튼
delete_btn = tk.Button(frame3_4, text="삭제")
delete_btn.pack(side="left")

# 권한에 따른 권한 부여/제한
# >> 사용자가 USER일 경우
# >> >> 추가, 저장, 삭제 버튼 비활성화
if (current_user["role"] == "user"):
    add_btn.config(state="disabled")
    save_btn.config(state="disabled")
    delete_btn.config(state="disabled")

# 이벤트 바인딩
# >> Treeview에서 항목 선택시 이벤트 발생
tree.bind("<<TreeviewSelect>>", lambda e: on_tree_select(tree, entry4, entry5, entry6, combo7, combo8, current_user, delete_btn))

root.mainloop()