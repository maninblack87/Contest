# routes/Router.py
import tkinter as tk
import subprocess

def run_main(master:tk.Widget):
    master.destroy()
    subprocess.run(["python", "views/viewMain.py"])
