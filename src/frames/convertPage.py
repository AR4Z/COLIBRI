import tkinter as tk
from tkinter import PhotoImage, filedialog, StringVar, Radiobutton
from tkinter.ttk import Progressbar
import tkinter.messagebox
import threading
from utils.utils import len_file_pdf, extract_text, text_to_audio, extract_name_audio, len_audio_file
from .audioPage import AudioPage


# tipo y numero de fuente
LARGE_FONT = ("Verdana", 12)


class ConvertPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # compartir info entre frames
        self.controller = controller
        self.name_audio = ""
        self.duration_audio_file = ""

        # boton para seleccionar archivo a convertir
        self.button_browse_file = tk.Button(self, text="EXAMINAR",
                                       command=self.select_pdf)
        self.button_browse_file.pack(pady=10)

        # label archivo
        self.label_file = tk.Label(self, text="ARCHIVO: ", font=LARGE_FONT)
        self.label_file.pack(pady=10, padx=10)

        # donde se va a guardar la ruta del pdf seleccionado para la conversion
        self.path_selected_file = tk.StringVar(None)

        # campo donde sera mostrada la ruta del pdf seleccionado
        self.field_path_selected_file = tk.Entry(self, width='65', textvariable=self.path_selected_file)
        self.field_path_selected_file.pack()

        self.option = StringVar()
        scanned = Radiobutton(self, text="PDF ESCANEADO", value="ocr", var=self.option)
        normal = Radiobutton(self, text="PDF NORMAL", value="pymupdf", var=self.option)

        scanned.pack()
        normal.pack()
        # numero de paginas
        self.until_number_page = tk.IntVar()
        self.from_number_page = tk.IntVar()

        # boton y label numero de pagina inicial
        self.label_from_number_page = tk.Label(self, text="DESDE: ", font=LARGE_FONT)
        self.field_from_number_page = tk.Entry(self, width='5', textvariable=self.from_number_page)
        self.label_from_number_page.pack()
        self.field_from_number_page.pack()

        # bboton y label numero de pagina final
        self.label_until_number_page = tk.Label(self, text="HASTA: ", font=LARGE_FONT)
        self.field_until_number_page = tk.Entry(self, width='5', textvariable=self.until_number_page)
        self.label_until_number_page.pack()
        self.field_until_number_page.pack()

        # slider para configurar la velocidad
        self.label_speed = tk.Label(self, text="VELOCIDAD: ", font=LARGE_FONT)
        self.label_speed.pack()
        self.scale_speed = tk.Scale(self, orient='horizontal', from_=80, to=450)
        self.scale_speed.set(175)
        self.scale_speed.pack()

        # slider para configurar el tono
        self.label_pitch = tk.Label(self, text="TONO: ", font=LARGE_FONT)
        self.label_pitch.pack()
        self.scale_pitch = tk.Scale(self, orient='horizontal', from_=0, to=99)
        self.scale_pitch.set(50)
        self.scale_pitch.pack()

        # boton para realizar la conversion
        self.button_conversion = tk.Button(self, text="CONVERTIR", command=self.conversion)
        self.button_conversion.pack(pady=20)

        # imagen y boton return
        self.icon_return = PhotoImage(file="../img/ic_home_black_24dp_1x.png")
        self.button_return = tk.Button(self, text="ATRÁS", command=lambda: self.controller.show_frame(self.controller.data["menu_frame"]),
                                  image=self.icon_return)
        self.button_return.pack(pady=10)

        # barra de progreso de conversion
        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, mode='indeterminate', takefocus=True)
        self.is_valid = False

    def select_pdf(self):
        """
            Se encarga de abrir el explorador de archivos para elegir el pdf a convertir.

        :return: None
        """
        # toma la ruta del file seleccionado
        selected_file = filedialog.askopenfilename(initialdir=self.controller.data["home_user"], title="SELECCIONAR LIBRO",
                                                   filetypes=(("archivos pdf", "*.pdf"), ("todos los archivos", "*.*")))
        # llena el campo con esa ruta para mostrarse en el frame
        self.path_selected_file.set(selected_file)
        # la primera pagina es 0
        self.from_number_page.set(0)
        # la ultima pagina es la longitud del pdf
        self.until_number_page.set(len_file_pdf(selected_file))

    def conversion(self):
        """
            Se encarga de ejecutar los hilos para realizar la conversion

        :return: None
        """
        self.validate()

        if self.is_valid:
            # muestra la barra para informar que el proceso se esta ejecutando
            self.show_progress(True)

            # bloquear botones mientras se realiza la conversion
            self.button_conversion.config(state='disabled')
            self.scale_pitch.config(state='disabled')
            self.scale_speed.config(state='disabled')
            self.button_browse_file.config(state='disabled')
            self.button_return.config(state='disabled')
        
            # crea un hilo para realizar la conversion que va a ser ejecutada por conversion_worker
            self.thread = threading.Thread(target=self.conversion_worker)
            self.thread.daemon = True
            self.thread.start()
            # verifica cuando termina el hilo
            self.conversion_check()
        else:
            return

    def conversion_check(self):
        """
            Se encarga de verificar cuando termina el hilo

        :return: None
        """

        # verifica si el hilo esta vivo, en caso contrario oculta la barra de proceso y muestra el frame de
        # reproducción de audio
        if self.thread.is_alive():
            self.after(10, self.conversion_check)
        else:
            self.show_progress(False)
            self.controller.show_frame(AudioPage)

    def conversion_worker(self):
        """
            Se encarga de realizar la conversión

        :return: None
        """
        #
        # extrae el texto y genera un .txt con el
        extract_text(self.field_path_selected_file.get(), self.from_number_page.get(), self.until_number_page.get(), self.option.get())
        self.controller.data["path_file"] = text_to_audio(self.scale_speed.get(),
                                                          extract_name_audio(self.field_path_selected_file.get()),
                                                          self.scale_pitch.get(), self.controller.data["path_audios"])
        # toma el nombre del audio y la duracion del archivo para ser guardado en base de datos
        self.name_audio = self.controller.data["path_file"]
        self.duration_audio_file = len_audio_file(self.controller.data["path_file"])
        #self.duration_audio_file = 0
        # inserta registro en db
        self.controller.data["manage_db"].add_file(self.name_audio, self.duration_audio_file)

    def show_progress(self, start):
        """
            muestra la barra de progreso

        :param start: True o False
        :return: None
        """
        if start:
            self.progress_bar.pack()
            self.progress_bar.start()
        else:
            self.progress_bar.stop()

    def error(self, message):
        tkinter.messagebox.showerror("Error", message)

    def validate(self):
        if self.field_path_selected_file.get() == "":
            self.error("SELECCIONE UN ARCHIVO")
            return

        if self.option.get() != "pymupdf" and self.option.get() != "ocr":
            self.error("ELIJA UN MODO DE CONVERSION")
            return

        if self.from_number_page.get() > self.until_number_page.get():
            self.error("LA PAGINA INICIAL NO PUEDE SER MAYOR QUE LA FINAL")
            return

        self.is_valid = True

