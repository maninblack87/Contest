import subprocess

def go_t2(current_window):
    current_window.destroy()  # 현재 창 닫기
    subprocess.Popen(["python", "t2.py"])  # t2.py 실행

def go_t3(root):
    root.withdraw()
    subprocess.Popen(["python", "t3.py"])

def go_t4(root):
    root.withdraw()
    subprocess.Popen(["python", "t4.py"])