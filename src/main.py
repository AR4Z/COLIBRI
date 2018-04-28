import tkinter as tk
from frames.menuPage import MenuPage
from utils.db import DBHelper
from pathlib import Path
import os
from utils.utils import create_directory, firstOnce, secondOnce
import zipfile
import ctypes
import time
import subprocess
import platform
from tkinter import ttk

if platform.system() == "Windows":
    from pywinauto.application import Application

# tipo y numero de fuente
LARGE_FONT = ("Verdana", 16)


class PdfToAudio(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(0, 0)
        self.container = tk.Frame(self)
        self.container.pack(side="top")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_propagate(0)

        self.s= ttk.Style()
        self.s.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'yellow'), ('!disabled', 'yellow')],
                  background=[('pressed', 'black'), ('active', 'black'), ('!disabled', 'black')]
                  )
        self.s.configure("TButton", font=LARGE_FONT)

        self.manage_db = DBHelper("audios")
        self.manage_db.create_table()
        self.home_user = Path.home()
        self.frames = {}
        self.data = {
            "path_file": "",
            "manage_db": self.manage_db,
            "home_user": self.home_user,
            "path_audios": os.path.join(self.home_user, "AudioLibros"),
            "menu_frame": MenuPage
        }
        create_directory(self.data["path_audios"])
        self.show_frame(MenuPage, 450, 250)

    def show_frame(self, cont, width, height):
        frame = cont(self.container, self)
        self.container["width"] = width
        self.container["height"] = height
        self.frames[cont] = frame
        print(self.frames)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_propagate(0)
        frame = self.frames[cont]
        frame.tkraise()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if firstOnce() == '0':
    print("Primera vez configurando")

    if not is_admin():
        # Re-run the program with admin rights
        # ctypes.windll.shell32.ShellExecuteEx(None, "runas", sys.executable,'main',None, 1)
        pass
    time.sleep(5)
    espeak_install = Application().start("bin/espeak.exe")
    subprocess.Popen([r"bin/vlc.exe"])
    # ocr_tool = Application().start("bin/tessereact.exe")

    with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
        zip_ref.extractall(os.path.join(Path.home(), "bin", "ffmpeg\\"))

    with zipfile.ZipFile("lame.zip", "r") as zip_ref:
        zip_ref.extractall(os.path.join(Path.home(), "bin", "lame\\"))

    secondOnce()

app = PdfToAudio()
app.title('pdfToAudio')
app.update()
app.mainloop()
