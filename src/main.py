from tkinter import Button, Tk, Listbox
import os


class PdfToAudio:
    def __init__(self, master):
        self.master = master
        self.master.geometry("430x200")
        self.master.title("PDF to Audio")
        self.master.resizable(0, 0)
        self.listbox = Listbox(self.master)
        self.newButton = Button(self.master, text="NUEVO", command=self.show_selection)
        self.newButton.place(x=180, y=30)
        self.showAudios = self.show_audios()


    def show_audios(self):
        self.listbox.place(x=10, y=100)
        self.listbox.insert(1, '<filename>')
        self.listbox.insert(2, '<filename>')
        self.listbox.insert(3, '<filename>')

    def show_selection(self):
        print("swsw")
        print(self.listbox.curselection())





root = Tk()
app = PdfToAudio(root)

root.mainloop()