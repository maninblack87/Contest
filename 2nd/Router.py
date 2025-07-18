import subprocess

def run_t2(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "t2.py"])

def run_t3(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "t3.py"])

def run_t4(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "t4.py"])