# Router.py
import subprocess

def open_t1(current_window):
    current_window.destroy()
    subprocess.run(["python", "t1.py"])

def open_t2(current_window):
    current_window.destroy()
    subprocess.run(["python", "t2.py"])

def open_t3(current_window):
    current_window.destroy()
    subprocess.run(["python", "t3.py"])

def open_t4(current_window):
    current_window.destroy()
    subprocess.run(["python", "t4.py"])