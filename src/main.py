import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import filedialog, PhotoImage
import glob
from src.utils.utils import text_to_audio, extract_text, extract_name_audio, len_file_pdf
import pygame
import threading

LARGE_FONT = ("Verdana", 12)


class PdfToAudio(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.data = {
            "path_file": "",
            "existing_audios": []
        }

        self.show_frame(MenuPage)

    def show_frame(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        button_convert = tk.Button(self, text="CONVERTIR TEXTO",
                                   command=lambda: controller.show_frame(ConvertPage))
        button_convert.pack(pady=10)

        label = tk.Label(self, text="AUDIOS EXISTENTES", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.listbox = tk.Listbox(self, width=59, height=5)
        self.listbox.pack(pady=5, padx=70)
        self.show_audios()

        button_open_audio_file = tk.Button(self, text="ABRIR AUDIO",
                            command=self.open_audio)

        button_open_audio_file.pack(pady=10)

        self.image_refresh = PhotoImage(file="../img/ic_refresh_black_24dp_1x.png")
        button_refresh_files = tk.Button(self, text="REFRESCAR", command=self.show_audios, image=self.image_refresh)
        button_refresh_files.pack()

    def show_audios(self):
        listAudios = glob.glob("/home/ar4z/Audiolibros/*.wav")
        for audio, n_audio in zip(listAudios, range(len(listAudios))):
            if not(audio in self.controller.data["existing_audios"]):
                print("sw", audio, n_audio)
                self.controller.data["existing_audios"].append(audio)
                self.listbox.insert(n_audio, audio)


    def open_audio(self):
        self.controller.data["path_file"] = self.listbox.get(self.listbox.curselection()[0])
        self.controller.show_frame(AudioPage)


class ConvertPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button_browse_file = tk.Button(self, text="EXAMINAR",
                            command=self.select_pdf)
        button_browse_file.pack(pady=10)

        label_file = tk.Label(self, text="ARCHIVO: ", font=LARGE_FONT)
        label_file.pack(pady=10, padx=10)

        self.path_selected_file = tk.StringVar(None)
        self.field_path_selected_file = tk.Entry(self, width='65', textvariable=self.path_selected_file)
        self.field_path_selected_file.pack()

        self.until_number_page = tk.IntVar()
        self.from_number_page = tk.IntVar()
        label_from_number_page = tk.Label(self, text="DESDE: ", font=LARGE_FONT)

        self.field_from_number_page = tk.Entry(self, width='5', textvariable=self.from_number_page)

        label_from_number_page.pack()
        self.field_from_number_page.pack()

        label_until_number_page = tk.Label(self, text="HASTA: ", font=LARGE_FONT)

        self.field_until_number_page = tk.Entry(self, width='5', textvariable=self.until_number_page)

        label_until_number_page.pack()
        self.field_until_number_page.pack()

        label_speed = tk.Label(self, text="VELOCIDAD: ", font=LARGE_FONT)
        label_speed.pack()

        self.scale_speed = tk.Scale(self, orient='horizontal', from_=80, to=450)
        self.scale_speed.set(175)
        self.scale_speed.pack()

        label_pitch = tk.Label(self, text="TONO: ", font=LARGE_FONT)
        label_pitch.pack()

        self.scale_pitch = tk.Scale(self, orient='horizontal', from_=0, to=99)
        self.scale_pitch.set(50)
        self.scale_pitch.pack()

        self.controller = controller

        button_conversion = tk.Button(self, text="CONVERTIR",
                            command=self.conversion)
        button_conversion.pack(pady=20)

        self.icon_return = PhotoImage(file="../img/ic_arrow_back_black_24dp_1x.png")
        button_return = tk.Button(self, text="ATRÁS", command=lambda: self.controller.show_frame(MenuPage), image=self.icon_return)
        button_return.pack(pady=10)

    def select_pdf(self):
        selected_file = filedialog.askopenfilename(initialdir="/home/ar4z", title="SELECCIONAR LIBRO",
                                                   filetypes=(("archivos pdf", "*.pdf"), ("todos los archivos", "*.*")))
        self.path_selected_file.set(selected_file)
        self.from_number_page.set(0)
        self.until_number_page.set(len_file_pdf(selected_file))

    def conversion(self):
        self.show_progress(True)
        self.thread = threading.Thread(target=self.conversion_worker)
        self.thread.daemon = True
        self.thread.start()
        self.conversion_check()

    def conversion_check(self):
        if self.thread.is_alive():
            self.after(10, self.conversion_check)

        else:
            self.show_progress(False)

    def conversion_worker(self):
        extract_text(self.field_path_selected_file.get(), self.from_number_page.get(), self.until_number_page.get())
        self.controller.data["path_file"] = text_to_audio(self.scale_speed.get(),
                                                          extract_name_audio(self.field_path_selected_file.get()),
                                                          self.scale_pitch.get())
        self.controller.show_frame(AudioPage)

    def show_progress(self, start):
        if start:
            self.progress_bar = Progressbar(self,orient=tk.HORIZONTAL,
                                                mode='indeterminate',
                                                takefocus=True)
            self.progress_bar.pack()
            self.progress_bar.start()
        else:

            self.progress_bar.stop()
            self.controller.show_frame(AudioPage)

    def get_name_file(self):
        return self.path_selected_file.get()


class AudioPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print(controller.data["path_file"])
        label_name_file = tk.Label(self, text=controller.data["path_file"], font=LARGE_FONT)

        label_name_file.pack(pady=10, padx=10)
        self.icon_play = PhotoImage(file="../img/ic_play_arrow_black_24dp_1x.png")
        self.icon_pause = PhotoImage(file="../img/ic_pause_black_24dp_1x.png")
        button_play = tk.Button(self, text="Reproducir",
                            command=lambda: self.play_audio(controller.data["path_file"]), image=self.icon_play)
        button_play.pack()

        button_pause = tk.Button(self, text="Pausa",
                            command=self.pause_audio, image=self.icon_pause)
        button_pause.pack()

    def play_audio(self, audio_file):
        print(audio_file)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        pygame.mixer.get_busy()

    def pause_audio(self):
        print("sw")
        pygame.mixer.music.pause()


app = PdfToAudio()
app.mainloop()