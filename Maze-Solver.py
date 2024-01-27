import Functions
import tkinter
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os
from PIL import Image,ImageTk
import threading

class MazeSolver:
    def __init__(self):
        # set global variables
        self.fun = Functions.maze_solver()
        self.thread = None
        self.mazeimg = None
        self.draw_player = False

        # setup GUI
        # setup main window
        self.root = tkinter.Tk()
        self.root.minsize(510,550)
        self.root.title("Maze Solver v1.0")
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
            test = self.fun.create_maze(file.name)
            if not test[0]:
                tkinter.messagebox.showerror("Error", test[1])
                self.loadButton.config(state=NORMAL)
            else:
                # load selected image to bord
                self.img= ImageTk.PhotoImage(Image.open(file.name))
                self.canvas.create_image(5, 5, image=self.img, anchor=NW)
                self.startButton.config(state=NORMAL)
    
    def start(self):
        # disable buttons
        self.loadButton.config(state=DISABLED)
        self.startButton.config(state=DISABLED)

        # start thread
        self.thread = threading.Thread(target=self.play)
        self.thread.daemon = True
        self.thread.start()

    def play(self):
        # setup
        win = False

        # run the algorythm until winning
        while not win:
            win = True
            if self.fun.Player[0] != self.fun.Target[0] or self.fun.Player[1] != self.fun.Target[1]: # player is not in the end pos
                win = False # do another step later
                self.fun.calculate_next_step() # calculate what step to take
                self.fun.move() # do the step
            self.fun.add_step(self.fun.Player[0],self.fun.Player[1],win) # write step to step log
            self.display_current_player_location()
        # end of the run
        self.fun.draw_path() # draw the chosen path 
        self.fun.draw_maze() # draw the rest of the maze
        self.img= ImageTk.PhotoImage(Image.open("result.png"))
        self.canvas.create_image(5, 5, image=self.img, anchor=NW)

        # enable buttons
        self.loadButton.config(state=NORMAL)
        self.startButton.config(state=NORMAL)
    
    def display_current_player_location(self):
        if not self.draw_player:
            self.draw_player = self.canvas.create_rectangle(0, 0, 10, 10, fill='red')
        else:
            self.canvas.tag_raise(self.draw_player)
            self.canvas.moveto(self.draw_player,self.fun.Player[0]-5,self.fun.Player[1]-5)

MazeSolver()