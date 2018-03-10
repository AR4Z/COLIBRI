import tkinter as tk
from tkinter import filedialog
import glob
from src.utils.utils import text_to_audio


LARGE_FONT = ("Verdana", 12)


class PdfToAudio(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button = tk.Button(self, text="CONVERTIR TEXTO",
                           command=lambda: controller.show_frame(PageOne))
        button.pack(pady=10)

        label = tk.Label(self, text="AUDIOS EXISTENTES", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.listbox = tk.Listbox(self, width=59, height=5)
        self.listbox.pack(pady=5, padx=70)
        self.show_audios()

        button2 = tk.Button(self, text="ABRIR AUDIO",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady=10)

    def show_audios(self):
        listAudios = glob.glob("/home/ar4z/Audiolibros/*.mp3")
        for audio, n_audio in zip(listAudios, range(len(listAudios))):
            print("sw", audio, n_audio)
            self.listbox.insert(n_audio, audio)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="EXAMINAR",
                            command=self.select_pdf)
        button1.pack(pady=10)
        label = tk.Label(self, text="ARCHIVO: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.path_selected_file = tk.StringVar(None)
        self.field_path_selected_file = tk.Entry(self, width='65', textvariable=self.path_selected_file)
        self.field_path_selected_file.pack()

        label = tk.Label(self, text="VELOCIDAD: ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.scale_speed = tk.Scale(self, orient='horizontal', from_=0, to=100)
        self.scale_speed.pack()

        button2 = tk.Button(self, text="CONVERTIR",
                            command=self.conversion)
        button2.pack(pady=50)

    def select_pdf(self):
        selected_file = filedialog.askopenfilename(initialdir="/home/ar4z", title="SELECCIONAR LIBRO", filetypes=(("archivos pdf","*.pdf"),("todos los archivos","*.*")))
        self.path_selected_file.set(selected_file)


    def conversion(self):
        text_to_audio(self.field_path_selected_file.get(), self.scale_speed.get())


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


app = PdfToAudio()
app.mainloop()