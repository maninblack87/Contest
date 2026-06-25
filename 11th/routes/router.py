import tkinter as tk
import subprocess

def route_w1(root:tk.Tk):
    root.destroy()
    subprocess.run(["python", "w1.py"])

def route_w2(root:tk.Tk):
    root.destroy()
    subprocess.run(["python", "w2.py"])

def route_w3(root:tk.Tk):
    root.destroy()
    subprocess.run(["python", "w3.py"])

def route_w4(root:tk.Tk):
    root.destroy()
    subprocess.run(["python", "w4.py"])