import tkinter as tk
import tkinter.messagebox
import glob
from .audioPage import AudioPage
from .convertPage import ConvertPage
from tkinter import ttk
# tipo y numero de fuente
LARGE_FONT = ("Verdana", 16)


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # boton para realizar conversiones
        button_convert = ttk.Button(self, text="CONVERTIR TEXTO",
                                   command=lambda: controller.show_frame(ConvertPage, 500, 400))
        button_convert.pack(pady=10)

        label = tk.Label(self, text="AUDIOS EXISTENTES", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # lista de archivos ya convertidos
        self.listbox = tk.Listbox(self, width=59, height=5)
        self.listbox.pack(pady=5, padx=70)
        # genera la lista
        self.show_audios()

        # boton para abrir el audio seleccionado
        button_open_audio_file = ttk.Button(self, text="ABRIR AUDIO",
                                           command=self.open_audio)

        button_open_audio_file.pack(pady=10)

    # funcion que me deuvlve todos los audios en la carpeta donde se guardan las conversiones
    def show_audios(self):
        # lista de archivos .mp3
        listAudios = glob.glob("{0}/*.mp3".format(self.controller.data["path_audios"]))
        for audio, n_audio in zip(listAudios, range(len(listAudios))):
            if not self.controller.data["manage_db"].get_file(audio) is None:
                print("sw", audio, n_audio)
                # agregando el elemento a la lista que se mostrara en la ventana
                self.listbox.insert(n_audio, audio)

    # function que se encarga de abrir un audio
    def open_audio(self):
        # obtiene la ruta del audio seleccionado
        try:
            self.controller.data["path_file"] = self.listbox.get(self.listbox.curselection()[0])
        except IndexError:
            tkinter.messagebox.showerror("ERROR", "SELECCIONE AUDIO")
        # abre el frame de audio
        self.controller.show_frame(AudioPage, 450, 200)