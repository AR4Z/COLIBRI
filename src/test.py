import os
import pygame
import tkinter
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import ttk

playlist = []
index = 0
paused = False

class Application(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.minsize(400,400)
        self.parent = parent
        self.main()

    def main(self):
        global v
        global songlabel
        global listbox
        global volumeslider
        global timeslider
        global time_elapsed
        global songlength

        self.configure(background='grey')
        self.grid()
        self.listbox = Listbox(self, width=20, height=25, relief='ridge', bd=3)
        self.listbox.grid(padx=30, pady=15, row=1, columnspan=11, sticky='NSEW')

        v = StringVar()
        songlabel = tkinter.Label(self, textvariable=v, width=30, anchor="n")

        rewbtn = PhotoImage(file="/home/ar4z/Projects/pdfToAudio/img/ic_arrow_back_black_24dp_1x.png")
        stopbtn = PhotoImage(file="/home/ar4z/Projects/pdfToAudio/img/ic_pause_black_24dp_1x.png")
        playbtn = PhotoImage(file="/home/ar4z/Projects/pdfToAudio/img/ic_play_arrow_black_24dp_1x.png")
        pausebtn = PhotoImage(file="/home/ar4z/Projects/pdfToAudio/img/ic_pause_black_24dp_1x.png")
        ffbtn = PhotoImage(file="/home/ar4z/Projects/pdfToAudio/img/ic_refresh_black_24dp_1x.png")

        prevbutton = Button(self, width=30, height=30, image=rewbtn, anchor='w')
        prevbutton.image = rewbtn
        prevbutton.bind("<Button-1>", self.prevsong)
        prevbutton.grid(row=10, column=0, padx=(30,0), sticky='w')

        playbutton = Button(self, width=30, height=30, image=playbtn, anchor='w')
        playbutton.image = playbtn
        playbutton.bind("<Button-1>", self.play)
        playbutton.grid(row=10, column=1, sticky='w')

        pausebutton = Button(self, width=30, height=30, image=pausebtn, anchor='w')
        pausebutton.image = pausebtn
        pausebutton.bind("<Button-1>", self.pause)
        pausebutton.grid(row=10, column=2, sticky='w')

        stopbutton = Button(self, width=30, height=30, image=stopbtn, anchor='w')
        stopbutton.image = stopbtn
        stopbutton.bind("<Button-1>", self.stop)
        stopbutton.grid(row=10, column=3, sticky='w')

        nextbutton = Button(self, width=30, height=30, image=ffbtn, anchor='w')
        nextbutton.image = ffbtn
        nextbutton.bind("<Button-1>", self.nextsong)
        nextbutton.grid(row=10, column=4, sticky='w')

        volumeslider = Scale(self, from_=0, to = 1, resolution = 0.01, orient = HORIZONTAL, showvalue = 'yes', command = self.change_vol)
        volumeslider.grid(row=10, column=8, columnspan=3, padx=30, pady=(0,10), sticky='wse')
        volumeslider.set(50)

        timeslider = Scale(self, from_=0, to=100, resolution=1, orient=HORIZONTAL, showvalue = 'no', command=self.cue)
        timeslider.grid(row=12, column=0, columnspan=11, padx = 30, sticky='wse')
        timeslider.set(0)

        time_elapsed = Label(text="0:00:00")
        time_elapsed.grid(row=13, columnspan=11, padx=(30,0), pady=(0,30), sticky='ws')
        # time_remaining = Label(text="0:00:00")
        # time_remaining.grid(row=13, column = 7, columnspan=5, padx=(0,30), pady=(0,30), sticky='se')

    # FILE OPEN
        self.directorychooser()
        playlist.reverse()
        for items in playlist:
            self.listbox.insert(0, items)
        playlist.reverse()
        self.listbox.bind("<Double-Button-1>", self.selectsong)
        self.listbox.bind("<Return>", self.selectsong)
        songlabel.grid(row = 0, column = 0, columnspan = 10, padx = 55, pady=(10,0), sticky=W+N+E)

    # GRID WEIGHT
        self.grid_columnconfigure(5,weight=1)
        self.grid_columnconfigure(7,weight=1)
        self.grid_rowconfigure(1,weight=1)


    def prevsong(self, event):
        global index

        if index > 0:
            index-=1
            print(index)
        elif index == 0:
            index = len(playlist)-1

        pygame.mixer.music.load(playlist[index])
        self.set_timescale()
        pygame.mixer.music.play()
        self.get_time_elapsed()
        self.update_timeslider()
        self.update_currentsong()


    def play(self, event):
        self.set_timescale()
        pygame.mixer.music.play()
        self.get_time_elapsed()
        self.update_timeslider()
        self.update_currentsong()


    def pause(self, event):
        global paused
        if paused == True:
            pygame.mixer.music.unpause()
            paused = False
        elif paused == False:
            pygame.mixer.music.pause()
            paused = True


    def nextsong(self, event):
        global index

        if index < len(playlist)-1:
            index+=1
        elif index == (len(playlist)-1):
            index = 0
        pygame.mixer.music.load(playlist[index])
        self.set_timescale()
        pygame.mixer.music.play()
        self.get_time_elapsed()
        self.update_timeslider()
        self.update_currentsong()


    def stop(self, event):
        pygame.mixer.music.stop()
        v.set("")
        return songlabel


    def selectsong(self, event):
        global index
        global songtime
        global songlength

        idx = self.listbox.curselection()
        index = idx[0]
        pygame.mixer.music.load(playlist[index])

        self.set_timescale()
        pygame.mixer.music.play()
        self.get_time_elapsed()
        # self.get_time_remaining()
        self.update_timeslider()
        self.update_currentsong()


    def change_vol(self, _ = None):
        pygame.mixer.music.set_volume(volumeslider.get())


    def cue(self, _ = None):
        pygame.mixer.music.set_pos(timeslider.get())


    def getsonglen(self):
        s = pygame.mixer.Sound(playlist[index])
        songlength = s.get_length()
        return songlength


    def set_timescale(self):
        songlength = self.getsonglen()
        timeslider.config(to=songlength)


    def get_time_elapsed(self):
        global time_elapsed
        time = int(pygame.mixer.music.get_pos()/1000)
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        clock = "%d:%02d:%02d" % (h, m, s)
        time_elapsed.configure(text=clock)
        self.after(100, self.get_time_elapsed)

    # def get_time_remaining(self):
    #   global time_remaining
    #   time = int(pygame.mixer.music.get_pos()/1000)
    #   songlen = int(self.getsonglen())
    #   rem = songlen - time
    #   m, s = divmod(rem, 60)
    #   h, m = divmod(m, 60)
    #   clock2 = "%d:%02d:%02d" % (h, m, s)
    #   time_remaining.configure(text=clock2)
    #   self.after(100, self.get_time_remaining)


    def update_timeslider(self, _ = None):
        time = (pygame.mixer.music.get_pos()/1000)
        timeslider.set(time)
        self.after(10, self.update_timeslider)


    def update_currentsong(self):
        global index
        global songlabel
        v.set(playlist[index])
        return songlabel


    def directorychooser(self):
        directory = askdirectory()
        os.chdir(directory)
        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                realdir = os.path.realpath(files)
                playlist.append(files)
                print(files)
        pygame.mixer.init()
        pygame.mixer.music.load(playlist[0])
        self.update_currentsong()

app = Application(None)
app.mainloop()