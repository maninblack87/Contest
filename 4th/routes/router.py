# routes/router.py
import subprocess
import sys

def run_w1(root):
    root.destroy()
    subprocess.run([sys.executable, "w1.py"])

def run_w2(root):
    root.destroy()
    subprocess.run([sys.executable, "w2.py"])

def run_w3(root):
    root.destroy()
    subprocess.run([sys.executable, "w3.py"])

def run_w4(root):
    root.destroy()
    subprocess.run([sys.executable, "w4.py"])