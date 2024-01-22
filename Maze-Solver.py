from PIL import Image as pilimg
import math
import tkinter
from tkinter import *
import tkinter.filedialog
import os
import threading

class MazeSolver:
    def __init__(self):
        # global vars 
        self.maze_location = None
        self.BOARD = {}
        self.player = [None,None]
        self.target = [None,None]
        self.startPoint = [None,None]
        self.next_cells = []
        self.thread = None
        self.colors = {"W": (0,0,0), "P":(0,162,232), "F":(237,28,36), " ":(255,255,255), "*":(222, 216, 35)}

        # start
        self.setup_gui()
    
    def setup_gui(self):
        # setup main window
        self.root = tkinter.Tk()
        self.root.geometry("640x480")
        self.root.minsize(640, 480)
        self.root.title("Maze Solver v1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap("favicon.ico")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # draw menu
        menuFrame = Frame(self.root)
        menuFrame.grid(column=0, row=0, sticky="news")
        self.loadButton = Button(menuFrame, text="Load", command=lambda: self.load())
        self.loadButton.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
        self.loadButton.config(width = 10)
        self.startButton = Button(menuFrame, text="Start", command=lambda: self.start())
        self.startButton.grid(column=1, row=0, padx=5, pady=5, sticky="nw")
        self.startButton.config(width = 10)
        self.startButton.config(state=DISABLED)

        # draw puzzle
        self.canvas = Canvas(self.root,bg='white')
        self.canvas.grid(column=0, row=1, padx=5, pady=5, columnspan=4, sticky="news")
        
        # run main loop
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        os._exit(1)

    def load(self):
        file = tkinter.filedialog.askopenfile(mode ='r', filetypes =[('Image Files', '*.png')])
        try:
            self.thread._stop()
        except:
            pass
        if file:
            self.maze_location = file.name
            self.create_maze()
            self.startButton.config(state=NORMAL)

    def start(self):
        self.thread = threading.Thread(target=self.process)
        self.thread.daemon = True
        self.startButton.config(state=DISABLED)
        self.loadButton.config(state=DISABLED)
        self.thread.start()
    
    def process(self):
        win = False
        while not win:
            #self.draw_maze()
            #input("Continue >")
            win = True
            if self.player[0] != self.target[0] or self.player[1] != self.target[1]:
                win = False
                # create next step cells, and evaluate the distance of each next cell
                self.create_next_cells()
                # move to the lowest distance cell, and make this cell blocket so it cannot be reused
                self.move()
                # now there is a tree of all paths player took, cut down all the unused branches
        self.draw_maze()
    
    def create_next_cells(self):
        directions = [(0,-1), (0,1), (-1,0), (1,0)]
        for cor in directions:
            x = self.player[0]+cor[0]
            y = self.player[1]+cor[1]
            # d=√((x_2-x_1)²+(y_2-y_1)²)
            delta = math.ceil(math.sqrt((self.target[0]-x)**2 + (self.target[1]-y)**2))
            loc = str(x)+":"+str(y)
            if self.BOARD[loc].obj != "W" and self.BOARD[loc].obj != "P" and self.BOARD[loc].obj != "*":
                self.next_cells.append((delta,x,y))
        self.next_cells.sort(reverse=True)
    
    def move(self):
        next_cell = self.next_cells.pop()
        delta = next_cell[0]
        x = next_cell[1]
        y = next_cell[2]
        loc1 = str(self.player[0])+":"+str(self.player[1])
        loc2 = str(x)+":"+str(y)
        self.BOARD[loc1].obj = "*"
        self.player[0] = x
        self.player[1] = y
        self.BOARD[loc2].obj = "P"
        #self.draw_maze()

    def create_maze(self):
        # load image
        im = pilimg.open(self.maze_location)
        pix = im.load()
        self.width = im.size[0]
        self.height = im.size[1]

        # convert image to list
        startPoint = False
        finishPoint = False
        for y in range(self.height):
            #old_display = display
            for x in range(self.width):
                color = pix[x,y]
                obj = " "
                
                # wall
                if color[0] == 0 and color[1] == 0 and color[2] == 0:
                    obj = "W"
                
                # start
                if not startPoint:
                    if color[0] == 0 and color[1] == 162 and color[2] == 232:
                        obj = "P"
                        self.player[0] = x
                        self.player[1] = y
                        self.startPoint[0] = x
                        self.startPoint[1] = y
                        startPoint = True
                
                # finish
                if not finishPoint:
                    if color[0] == 237 and color[1] == 28 and color[2] == 36:
                        obj = "F"
                        self.target[0] = x
                        self.target[1] = y
                        finishPoint = True
                
                # add cell to board
                loc = str(x)+":"+str(y)
                self.BOARD[loc] = Cell(x,y,obj)
        #self.draw_maze()
    
    def draw_maze(self):
        display = []
        for y in range(self.height):
            for x in range(self.width):
                loc = str(x)+":"+str(y)
                start_loc = str(self.startPoint[0])+":"+str(self.startPoint[1])
                end_loc = str(self.target[0])+":"+str(self.target[1])
                cell = self.BOARD[loc]
                if loc != start_loc and loc != end_loc:
                    obj = cell.obj
                else:
                    if loc == start_loc:
                        obj = "P"
                    elif loc == end_loc:
                        obj = "F"
                add = self.colors[obj]
                display.append(add)
        new_im = pilimg.new("RGB",(self.width,self.height))
        new_im.putdata(display)
        new_im.show()
        new_im.save("result.png")

class Cell:
    def __init__(self,x,y,obj):
        self.x = x
        self.y = y
        self.obj = obj

MazeSolver()