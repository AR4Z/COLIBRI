import tkinter as tk
import glob
from tkinter import PhotoImage
from .audioPage import AudioPage
from .convertPage import ConvertPage

# tipo y numero de fuente
LARGE_FONT = ("Verdana", 12)

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # boton para realizar conversiones
        button_convert = tk.Button(self, text="CONVERTIR TEXTO",
                                   command=lambda: controller.show_frame(ConvertPage))
        button_convert.pack(pady=10)

        label = tk.Label(self, text="AUDIOS EXISTENTES", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # lista de archivos ya convertidos
        self.listbox = tk.Listbox(self, width=59, height=5)
        self.listbox.pack(pady=5, padx=70)
        # genera la lista
        self.show_audios()

        # boton para abrir el audio seleccionado
        button_open_audio_file = tk.Button(self, text="ABRIR AUDIO",
                                           command=self.open_audio)

        button_open_audio_file.pack(pady=10)

        # boton para actualizar los archivos existentes
        self.image_refresh = PhotoImage(file="../img/ic_refresh_black_24dp_1x.png")
        button_refresh_files = tk.Button(self, text="REFRESCAR", command=self.show_audios, image=self.image_refresh)
        button_refresh_files.pack()

    # funcion que me deuvlve todos los audios en la carpeta donde se guardan las conversiones
    def show_audios(self):
        # lista de archivos .mp3
        listAudios = glob.glob("/home/ar4z/Audiolibros/*.mp3")
        for audio, n_audio in zip(listAudios, range(len(listAudios))):
            if not (audio in self.controller.data["existing_audios"]):
                print("sw", audio, n_audio)
                # agregando el elemento a los audios existentes
                self.controller.data["existing_audios"].append(audio)
                # agregando el elemento a la lista que se mostrara en la ventana
                self.listbox.insert(n_audio, audio)

    # function que se encarga de abrir un audio
    def open_audio(self):
        # obtiene la ruta del audio seleccionado
        self.controller.data["path_file"] = self.listbox.get(self.listbox.curselection()[0])
        # abre el frame de audio
        self.controller.show_frame(AudioPage)