# routes/Router.py
import subprocess

def run_w1(root):
    root.destroy()
    subprocess.run(["python", "w1.py"])

def run_w2(root):
    root.destroy()
    subprocess.run(["python", "w2.py"])

def run_w3(root):
    root.destroy()
    subprocess.run(["python", "w3.py"])

def run_w4(root):
    root.destroy()
    subprocess.run(["python", "w4.py"])