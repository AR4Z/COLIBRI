import tkinter as tk
from .convertEspeak import ConvertEspeak
from .convertGtts import ConvertGtts
import platform
# tipo y numero de fuente
LARGE_FONT = ("Verdana", 16)


class ConvertPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="TIPO DE VOZ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        if platform.system() == "Windows":
            height = 500
            height_gtts = 440
        else:
            height = 480
            height_gtts = 420
        # boton para seleccionar archivo a convertir
        self.button_mode_espeak=tk.Button(self, text="ROBOTICA",
                                       command=lambda:  self.controller.show_frame(ConvertEspeak, 500, height), font=LARGE_FONT, bg="#000000", fg="#ffff00", activebackground="#000000", activeforeground="#ffff00")
        self.button_mode_espeak.pack()

        self.button_mode_gtts = tk.Button(self, text="HUMANA",
                                            command=lambda: self.controller.show_frame(ConvertGtts, 500, height_gtts), font=LARGE_FONT, bg="#000000", fg="#ffff00",
                                            activebackground="#000000", activeforeground="#ffff00")
        self.button_mode_gtts.pack()
