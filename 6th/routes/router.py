import subprocess
import tkinter as tk

def route_w1(current_window:tk.Tk):
    current_window.destroy()
    subprocess.run(["python", "w1.py"])

def route_w2(current_window:tk.Tk):
    current_window.destroy()
    subprocess.run(["python", "w2.py"])

def route_w3(current_window:tk.Tk):
    current_window.destroy()
    subprocess.run(["python", "w3.py"])

def route_w4(current_window:tk.Tk):
    current_window.destroy()
    subprocess.run(["python", "w4.py"])