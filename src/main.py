import tkinter as tk
from frames.menuPage import MenuPage
from utils.db import DBHelper
from pathlib import Path
import os
from utils.utils import create_directory

# tipo y numero de fuente
LARGE_FONT = ("Verdana", 12)


class PdfToAudio(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.manage_db = DBHelper("audios")
        self.manage_db.create_table()
        self.home_user = Path.home()
        self.frames = {}
        self.data = {
            "path_file": "",
            "existing_audios": [],
            "manage_db": self.manage_db,
            "home_user": self.home_user,
            "path_audios": os.path.join(self.home_user, "AudioLibros")

        }

        create_directory(self.data["path_audios"])
        self.show_frame(MenuPage)

    def show_frame(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()


app = PdfToAudio()
app.mainloop()
