import tkinter as tk
from frames.menuPage import MenuPage
from utils.db import DBHelper
from pathlib import Path
import os
from utils.utils import create_directory
import platform

# tipo y numero de fuente
LARGE_FONT = ("Verdana", 16, 'bold')


class PdfToAudio(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(0, 0)
        self.container = tk.Frame(self)
        self.container.pack(side="top")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_propagate(0)

        self.manage_db = DBHelper("audios")
        self.manage_db.create_table()
        self.home_user = Path.home()
        self.frames = {}
        self.data = {
            "path_file": "",
            "name_file":"",
            "manage_db": self.manage_db,
            "home_user": self.home_user,
            "path_audios": os.path.join(self.home_user, "AudioLibros"),
            "menu_frame": MenuPage
        }
        create_directory(self.data["path_audios"])
        if platform.system() == "Windows":
            self.show_frame(MenuPage, 450, 350)
        else:
            self.show_frame(MenuPage, 450, 300)

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


app = PdfToAudio()
app.title('pdfToAudio')
app.update()
app.mainloop()
