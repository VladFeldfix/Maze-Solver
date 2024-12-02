import Functions
import tkinter
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os

class MazeSolver:
    def __init__(self):
        # set global vars
        self.fun = Functions.functions()

        # initiate
        self.setup_gui()
    
    def setup_gui(self):
        # setup main window
        self.root = tkinter.Tk()
        self.root.minsize(510,550)
        self.root.title("Maze Solver v2.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap("favicon.ico")
        self.root.resizable(False, False)

        # draw main menu
        menuFrame = Frame(self.root)
        menuFrame.grid(column=0, row=0, sticky="news")
        self.loadButton = Button(menuFrame, text="Load", command=lambda: self.load())
        self.loadButton.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
        self.loadButton.config(width = 10)
        self.startButton = Button(menuFrame, text="Start", command=lambda: self.start())
        self.startButton.grid(column=1, row=0, padx=5, pady=5, sticky="nw")
        self.startButton.config(width = 10)
        self.startButton.config(state=DISABLED)

        # darw maze
        self.canvas = Canvas(self.root,bg='white', width=500, height=500)
        self.canvas.grid(column=0, row=1, padx=5, pady=5, columnspan=3, sticky="news")
        
        # run GUI
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        os._exit(1)
    
    def load(self):
        # stop current thread
        try:
            self.thread._stop()
        except:
            pass
        
        # load a maze file
        file = tkinter.filedialog.askopenfile(mode ='r', filetypes =[('PNG Files', '*.png')])
        if file:
            self.startButton.config(state=DISABLED)
            self.fun.reset()
            test = self.fun.build_maze(file.name)
            if not test[0]:
                tkinter.messagebox.showerror("Error", test[1])
                self.loadButton.config(state=NORMAL)
            else:
                # load selected image to bord
                self.img = ImageTk.PhotoImage(Image.open("maze.png"))
                self.canvas.create_image(5, 5, image=self.img, anchor=NW)
                self.startButton.config(state=NORMAL)

    
MazeSolver()