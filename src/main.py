import tkinter as tk
from tkinter import filedialog, PhotoImage
from tkinter.ttk import Progressbar
import glob, vlc, time, threading, sqlite3
from utils.utils import text_to_audio, extract_text, extract_name_audio, \
    len_file_pdf, len_audio_file, seconds_in_time_for_humans

# tipo y numero de fuente
LARGE_FONT = ("Verdana", 12)


class PdfToAudio(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # base de datos
        con = sqlite3.connect("audios")
        self.cursor = con.cursor()
        sentences = ["""
            CREATE TABLE IF NOT EXISTS archivos(
              name TEXT NOT NULL,
              duracion TEXT NOT NULL
            )
        """]
        for sentence in sentences:
            self.cursor.execute(sentence)

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
            if not(audio in self.controller.data["existing_audios"]):
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


class ConvertPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # compartir info entre frames
        self.controller = controller
        self.name_audio = ""
        self.duration_audio_file = ""

        # boton para seleccionar archivo a convertir
        button_browse_file = tk.Button(self, text="EXAMINAR",
                            command=self.select_pdf)
        button_browse_file.pack(pady=10)

        # label archivo
        self.label_file = tk.Label(self, text="ARCHIVO: ", font=LARGE_FONT)
        self.label_file.pack(pady=10, padx=10)

        # donde se va a guardar la ruta del pdf seleccionado para la conversion
        self.path_selected_file = tk.StringVar(None)

        # campo donde sera mostrada la ruta del pdf seleccionado
        self.field_path_selected_file = tk.Entry(self, width='65', textvariable=self.path_selected_file)
        self.field_path_selected_file.pack()

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
        button_conversion = tk.Button(self, text="CONVERTIR", command=self.conversion)
        button_conversion.pack(pady=20)

        # imagen y boton return
        self.icon_return = PhotoImage(file="../img/ic_arrow_back_black_24dp_1x.png")
        button_return = tk.Button(self, text="ATRÁS", command=lambda: self.controller.show_frame(MenuPage), image=self.icon_return)
        button_return.pack(pady=10)

        # barra de progreso de conversion
        self.progress_bar = Progressbar(self, orient=tk.HORIZONTAL, mode='indeterminate', takefocus=True)

    def select_pdf(self):
        """
            Se encarga de abrir el explorador de archivos para elegir el pdf a convertir.

        :return: None
        """
        # toma la ruta del file seleccionado
        selected_file = filedialog.askopenfilename(initialdir="/home/ar4z", title="SELECCIONAR LIBRO",
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
        # muestra la barra para informar que el proceso se esta ejecutando
        self.show_progress(True)

        # crea un hilo para realizar la conversion que va a ser ejecutada por conversion_worker
        self.thread = threading.Thread(target=self.conversion_worker)
        self.thread.daemon = True
        self.thread.start()
        # verifica cuando termina el hilo
        self.conversion_check()

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
        self.controller.data["path_file"] = text_to_audio(self.scale_speed.get(),
                                                          extract_name_audio(self.field_path_selected_file.get()),
                                                          self.scale_pitch.get())
        # toma el nombre del audio y la duracion del archivo para ser guardado en base de datos
        self.name_audio = self.controller.data["path_file"].split('/')[-1]
        self.duration_audio_file = len_audio_file(self.controller.data["path_file"])
        # inserta registro en db
        self.insert_file_in_db(self.name_audio, self.duration_audio_file)


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

    def insert_file_in_db(self, name_file, duration):
        """
            Inserta el audio creado en la db
        :param name_file: Nombre del archivo .mp3 creado
        :param duration: duracion del archivo .mp3
        :return: None
        """
        con = sqlite3.connect("audios")
        cursor = con.cursor()
        sentences = ["""

                    INSERT INTO archivos
                    (name, duracion)
                    VALUES
                    (?,?)
                """]

        for sentence in sentences:
            cursor.execute(sentence, [name_file, duration])

        con.commit()


class AudioPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print(controller.data["path_file"])
        label_name_file = tk.Label(self, text=controller.data["path_file"], font=LARGE_FONT)

        label_name_file.pack(pady=10, padx=10)

        bd = sqlite3.connect("audios")
        self.cursor = bd.cursor()
        self.name_busqueda = controller.data["path_file"].split("/")[-1]
        sentencia = "SELECT * FROM archivos WHERE name LIKE?;"
        self.cursor.execute(sentencia, ["{}".format(self.name_busqueda)])
        audio = self.cursor.fetchone()
        print("audos", audio)
        print(float(audio[1]))
        self.len_current_audio_book = float(audio[1])
        self.timeslider = tk.Scale(self, from_=0, to=self.len_current_audio_book, resolution=1, orient=tk.HORIZONTAL,
                                   showvalue='no')
        self.timeslider.pack()
        self.timeslider.set(0)

        print("s",self.timeslider)

        self.time_elapsed = tk.Label(text=seconds_in_time_for_humans(self.timeslider.get()))
        self.time_elapsed.pack()
        self.icon_play = PhotoImage(file="../img/ic_play_arrow_black_24dp_1x.png")
        self.icon_pause = PhotoImage(file="../img/ic_pause_black_24dp_1x.png")
        self.icon_stop = PhotoImage(file="../img/ic_stop_black_24dp_1x.png")
        self.button_play = tk.Button(self, text="Reproducir",
                            command=lambda: self.play_audio(), image=self.icon_play)
        self.button_play.pack()

        self.button_stop = tk.Button(self, text="DETENER",
                                     command=lambda: self.replay(), image=self.icon_stop)

        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.media = self.Instance.media_new(controller.data["path_file"])
        self.pause = False
        self.play = False
        self.update_time_elapsed()


    def play_audio(self):
        print("play_audio")
        self.change_image_button_play(True)
        self.different_time = int(self.timeslider.get())* 1000
        print("differet: ", self.different_time)
        self.thread = threading.Thread(target=lambda: self.play_worker(self.different_time))
        print("thread vivo?", self.thread.is_alive())
        self.thread.daemon = True
        self.thread.start()
        print("thread vivo?", self.thread.is_alive())
        self.play_check()

    def play_worker(self, other_time):
        if (self.pause):
            self.player.pause()
            self.pause = False
            time.sleep(2)
            while self.player.is_playing():
                pass
            return
        self.player.set_media(self.media)
        self.player.play()
        self.player.set_time(other_time)
        time.sleep(2)
        while self.player.is_playing():
            pass


    def play_check(self):
        print("check")
        if self.thread.is_alive():
            print("vivo")
            self.update_time_slider()
            #self.different_time = self.len_current_audio_book - self.timeslider.get()
            self.after(10, self.play_check)
        else:
            self.change_image_button_play(False)

    def replay(self):
        self.play_audio()

    def change_image_button_play(self, start):
        if start:
            self.button_play.config(image=self.icon_pause, command=lambda: self.pause_audio())
        else:
            print("cambiando imagen")
            self.button_play.config(image=self.icon_play, command=lambda:self.play_audio())

    def pause_audio(self):
        print("PAUSE")
        self.player.pause()
        self.pause = True

    def stop_audio(self):
        print("stoping")
        pygame.mixer.music.stop()
        self.timeslider.set(0)
        self.time_elapsed.config(text=seconds_in_time_for_humans(0))
        print("pos after stop", self.timeslider.get())

    def update_time_elapsed(self):
        #print("update time elapsed")
        self.time_elapsed.config(text=seconds_in_time_for_humans(self.timeslider.get()))
        self.after(10, self.update_time_elapsed)

    def update_time_slider(self):
        print("update: ", self.player.get_time())
        self.timeslider.set(self.player.get_time()/1000)

    def set_time_play(self):
        self.player.set_time(self.timeslider.get()*1000)



app = PdfToAudio()
app.mainloop()


