import tkinter as tk
from tkinter import PhotoImage, filedialog, StringVar, Radiobutton, IntVar
from tkinter.ttk import Progressbar
import tkinter.messagebox
import threading
from utils.utils import len_file_pdf, extract_text, text_to_audio, extract_name_audio, len_audio_file
from .audioPage import AudioPage
import platform

# tipo y numero de fuente
LARGE_FONT = ("Verdana", 16)


class ConvertGtts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # compartir info entre frames

        self.controller = controller
        self.duration_audio_file = ""

        # boton para seleccionar archivo a convertir
        self.button_browse_file = tk.Button(self, text="EXAMINAR",
                                            command=self.select_pdf, font=LARGE_FONT, bg="#000000", fg="#ffff00",
                                            activebackground="#000000", activeforeground="#ffff00")
        self.button_browse_file.pack()

        # label archivo
        self.label_file = tk.Label(self, text="ARCHIVO: ", font=LARGE_FONT)
        self.label_file.pack()

        # donde se va a guardar la ruta del pdf seleccionado para la conversion
        self.path_selected_file = tk.StringVar(None)

        # campo donde sera mostrada la ruta del pdf seleccionado
        self.field_path_selected_file = tk.Entry(self, width='65', textvariable=self.path_selected_file,
                                                 font=LARGE_FONT)
        self.field_path_selected_file.pack()

        self.option_type_conversion = StringVar()
        self.label_conversion = tk.Label(self, text="TIPO DE CONVERSIÓN: ", font=LARGE_FONT)
        self.label_conversion.pack()
        scanned = Radiobutton(self, text="PDF ESCANEADO", value="ocr", var=self.option_type_conversion)
        normal = Radiobutton(self, text="PDF NORMAL", value="pymupdf", var=self.option_type_conversion)

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

        # nombre archivo
        self.name_conversion = tk.StringVar()
        self.label_name = tk.Label(self, text="NOMBRE: ", font=LARGE_FONT)
        self.field_name_conversion = tk.Entry(self, width='40', textvariable=self.name_conversion, font=LARGE_FONT)
        self.label_name.pack()
        self.field_name_conversion.pack()

        # slider para configurar la velocidad
        self.label_speed = tk.Label(self, text="VELOCIDAD: ", font=LARGE_FONT)
        self.label_speed.pack()
        self.scale_speed = tk.Scale(self, orient='horizontal', from_=1, to=2, activebackground="black", bg="#ffff00", resolution=0.1)
        self.scale_speed.set(1.5)
        self.scale_speed.pack()

        # boton para realizar la conversion
        self.button_conversion = tk.Button(self, text="CONVERTIR", command=self.conversion, font=LARGE_FONT,
                                           bg="#000000", fg="#ffff00", activebackground="#000000",
                                           activeforeground="#ffff00")
        self.button_conversion.pack()

        # imagen y boton return
        if platform.system() == "Windows":
            height = 380
            self.icon_return = PhotoImage(file="img/ic_home_black_24dp_1x.png")
        else:
            height = 380
            self.icon_return = PhotoImage(file="../img/ic_home_black_24dp_1x.png")

        self.button_return = tk.Button(self, text="ATRÁS",
                                       command=lambda: self.controller.show_frame(self.controller.data["menu_frame"],
                                                                                  450, height),
                                       image=self.icon_return)
        self.button_return.pack()

        # barra de progreso de conversion
        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, mode='indeterminate', takefocus=True)
        self.is_valid = False




    def select_pdf(self):
        """
            Se encarga de abrir el explorador de archivos para elegir el pdf a convertir.

        :return: None
        """
        # toma la ruta del file seleccionado
        selected_file = filedialog.askopenfilename(initialdir=self.controller.data["home_user"],
                                                   title="SELECCIONAR LIBRO",
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
            self.controller.show_frame(AudioPage, 450, 200)

    def conversion_worker(self):
        """
            Se encarga de realizar la conversión

        :return: None
        """
        #
        # extrae el texto y genera un .txt con el
        extract_text(self.field_path_selected_file.get(), self.from_number_page.get(), self.until_number_page.get(),
                     self.option_type_conversion.get())
        self.controller.data["path_file"] = text_to_audio(self.scale_speed.get(),
                                                          self.name_conversion.get(),
                                                          0, self.controller.data["path_audios"],
                                                          "gtts")
        # toma el nombre del audio y la duracion del archivo para ser guardado en base de datos
        path_audio = self.controller.data["path_file"]
        duration_audio_file = len_audio_file(self.controller.data["path_file"])

        # inserta registro en db
        self.controller.data["manage_db"].add_file(self.name_conversion.get(), duration_audio_file, path_audio)
        self.controller.data["name_file"] = self.name_conversion.get()

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

        if self.option_type_conversion.get() != "pymupdf" and self.option_type_conversion.get() != "ocr":
            self.error("ELIJA UN MODO DE CONVERSION")
            return

        if self.from_number_page.get() > self.until_number_page.get():
            self.error("LA PAGINA INICIAL NO PUEDE SER MAYOR QUE LA FINAL")
            return
        if self.name_conversion.get() == "":
            self.error("INGRESE UN NOMBRE PARA EL ARCHIVO")
            return
        if not self.controller.data["manage_db"].get_file(self.name_conversion.get()) is None:
            self.error("EL NOMBRE YA HA SIDO USADO")
            return
        self.is_valid = True
