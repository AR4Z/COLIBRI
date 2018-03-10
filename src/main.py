from tkinter import Button, Tk, Listbox, Frame
from src.utils.utils import list_files

class PdfToAudio:
    def __init__(self, master):
        # ventana principal
        self.master = master
        # medida ventana principal
        self.master.geometry("430x200")
        # nombre ventana principal
        self.master.title("PDF to Audio")
        # la ventana no puede cambiar de tamaño
        self.master.resizable(0, 0)

        # lista de archivos ya convertidos
        self.listbox = Listbox(self.master, width=59, height=5)
        # ubicacion dentro de la ventana de la lista de archivos
        self.listbox.place(x=5, y=70)

        # boton para realizar una nueva conversion
        self.newButton = Button(self.master, text="NUEVO", command=self.new_conversion)
        self.newButton.place(x=180, y=30)

        # boton para realizar una nueva conversion
        self.openButton= Button(self.master, text="ABRIR", command=self.show_selection)
        self.openButton.place(x=180, y=150)

        # muestra los libros o el material ya convetido
        self.showAudios = self.show_audios()


    def show_audios(self):
        listAudios = list_files("/home/ar4z/Audiolibros/*.mp3")
        for audio, n_audio in zip(listAudios, range(len(listAudios))):
            print("sw",audio, n_audio)
            self.listbox.insert(n_audio, audio)


    def show_selection(self):
        print(self.listbox.curselection())


    def new_conversion(self):
        
        frame = Frame(self.master)
        frame.pack()






root = Tk()
app = PdfToAudio(root)

root.mainloop()