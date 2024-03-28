"""PythonTest.py
"""

import sys
import os
import time
import tkinter
import tkinter.messagebox

root = tkinter.Tk()
def on_closing():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()