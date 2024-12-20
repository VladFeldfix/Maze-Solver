# imports
import tkinter
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os
from PIL import Image,ImageTk
import threading
import math

class Cell:
    def __init__(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.x = None
        self.y = None
        self.distance = None
        self.celltype = None
        self.goto = None
        self.prev = None
        self.blocked = False

class MazeSolver:
    def __init__(self):
        # GLOBAL VARS
        self.board = []
        self.start_point = ()
        self.finish_point = ()
        self.width = 0
        self.heigth = 0
        self.smallest_distance = 0
        self.colors = {" ":(255,255,255), "S":(255,0,0), "F":(0,0,255), "█":(0,0,0), "*":(0,255,0), "U":(255,255,0)}

        # START
        self.SetupGui()
    
    def SetupGui(self):
        # SETUP WINDOW
        self.root = tkinter.Tk()
        self.root.minsize(510,550)
        self.root.title("Maze Solver v2.0")
        self.root.protocol("WM_DELETE_WINDOW", self.Exit)
        self.root.iconbitmap("favicon.ico")
        self.root.resizable(False, False)

        # SETUP MAIN MENU
        menu_frame = Frame(self.root)
        menu_frame.grid(column=0, row=0, sticky="news")
        self.load_button = Button(menu_frame, text="Load", command=lambda: self.Load())
        self.load_button.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
        self.load_button.config(width = 10)
        self.start_button = Button(menu_frame, text="Start", command=lambda: self.Start())
        self.start_button.grid(column=1, row=0, padx=5, pady=5, sticky="nw")
        self.start_button.config(width = 10)
        self.start_button.config(state=DISABLED)

        # SETUP MAZE WINDOW 
        self.canvas = Canvas(self.root,bg='white', width=500, height=500)
        self.canvas.grid(column=0, row=1, padx=5, pady=5, columnspan=3, sticky="news")
        
        # RUN GUI
        self.root.mainloop()
    
    def Load(self):
        # STOP CURRENTLY RUNNING THREAD
        try:
            self.thread._stop()
        except:
            pass

        # GET IMAGE FILE
        file = tkinter.filedialog.askopenfile(mode ='r', filetypes =[('PNG Files', '*.png')])
        if not file:
            return

        # GENERATE MAP BASED ON THE IMAGE
        # setup local variables
        mazePNG = []
        error = ""

        # read img pixels
        img = Image.open(file.name)
        pix = img.load()

        # get width, height, and the largest distance in the board
        self.width = img.size[0]
        self.heigth = img.size[1]
        self.smallest_distance = math.sqrt(self.width**2+self.heigth**2)   
        
        # read every pixel on the img
        for y in range(self.heigth):
            # add row to board
            self.board.append([])

            for x in range(self.width):
                # determine the nature of the cell 
                # <   empty > 
                # < S start >
                # < F finish >
                # < █ wall >

                cell = " "
                value = pix[x,y]
                red = value[0]
                green = value[1]
                blue = value[2]

                # start point
                if red == 255 and green == 0 and blue == 0:
                    if len(self.start_point) == 0:
                        cell = 'S'
                        self.start_point = (x,y)
                
                # finish point
                if red == 0 and green == 0 and blue == 255:
                    if len(self.finish_point) == 0:
                        cell = 'F'
                        self.finish_point = (x,y)
                
                # wall
                if cell == " ":
                    if red < 255/2:
                        cell = '█'

                # add cell to board
                self.board[y].append(cell)

                # add cell to mazePNG
                mazePNG.append(self.colors[cell])
        
        # TEST MAP FOR CORRECTNESS <START POINT, FINISH POINT, WALLS, SIZE>
        if len(self.start_point) == 0:
            error = "Missing start point (Make sure that at leat one pixel is RGB colored [255,0,0])"
        if len(self.finish_point) == 0:
            error = "Missing finish point (Make sure that at leat one pixel is RGB colored [0,0,255])"
        if self.width > 500 or self.heigth > 500:
            error = "This image is too large. Maximum size is 500x500 px"
        
        # IN NO ERRORS THEN SAVE MAP AS maze.png ELSE SHOW AN ERROR MESSAGE
        if error == "":
            # generate image
            img = Image.new('RGB', (self.width, self.heigth))
            img.putdata(mazePNG)
            img.save('maze.png')

            # enable start button
            self.start_button.config(state=NORMAL)
        else:
            tkinter.messagebox.showerror("Error", error)
            self.load_button.config(state=NORMAL)
            return

        # LOAD MAP PROJECTION OTNO THE SCREEN
        self.mazePNG = ImageTk.PhotoImage(Image.open("maze.png"))
        self.canvas.create_image(2, 2, image=self.mazePNG, anchor=NW)
        self.start_button.config(state=NORMAL)
        
        # SETUP POINTER
        self.pointer = self.canvas.create_oval(2,2,10,10, fill='red', width=0)
        self.canvas.coords(self.pointer, self.start_point[0]-4, self.start_point[1]-4, self.start_point[0]+4, self.start_point[1]+4)

    def Start(self):
        # DISABLE BUTTONS
        self.load_button.config(state=DISABLED)
        self.start_button.config(state=DISABLED)

        # START THREAD
        self.thread = threading.Thread(target=self.Play)
        self.thread.daemon = True
        self.thread.start()
    
    def Play(self):
        # SETUP LOCAL VARIABLES
        solved = False
        pointer = Cell()

        # RUN LOOP UNTIL THE MAZE IS SOLVED
        # goto start point
        pointer.x = self.start_point[0]
        pointer.y = self.start_point[1]
        pointer.distance = self.CalculateDistanceToFinishline(pointer.x, pointer.y)

        # start solving loop
        while not solved:
            if pointer == None:
                tkinter.messagebox.showerror("Error", "This maze cannot be solved")
                self.load_button.config(state=NORMAL)
                return

            # reset pointer
            smallest_distance = self.smallest_distance
            pointer.goto = None

            # test 4 adjacent points
            for direction in ("UP", "DOWN", "LEFT", "RIGHT"):
                if direction == "UP":
                    testX = pointer.x
                    testY = pointer.y-1
                    pointer.up = Cell()
                    pointer.up.x = testX
                    pointer.up.y = testY
                    pointer.up.down = pointer
                    pointer.up.distance = self.CalculateDistanceToFinishline(pointer.up.x, pointer.up.y)
                    if testY >= 0:
                        pointer.up.celltype = self.board[testY][testX]
                    else:
                        pointer.up.celltype = "BORDER"
                    if pointer.up.celltype == " ":
                        if pointer.up.distance < smallest_distance:
                            if not pointer.up.blocked:
                                smallest_distance = pointer.up.distance
                                pointer.goto = pointer.up
                                pointer.up.prev = pointer
                
                if direction == "DOWN":
                    testX = pointer.x
                    testY = pointer.y+1
                    pointer.down = Cell()
                    pointer.down.x = testX
                    pointer.down.y = testY
                    pointer.down.up = pointer
                    pointer.down.distance = self.CalculateDistanceToFinishline(pointer.down.x, pointer.down.y)
                    if testY < len(self.board):
                        pointer.down.celltype = self.board[testY][testX]
                    else:
                        pointer.down.celltype = "BORDER"
                    if pointer.down.celltype == " ":
                        if pointer.down.distance < smallest_distance:
                            if not pointer.down.blocked:
                                smallest_distance = pointer.down.distance
                                pointer.goto = pointer.down
                                pointer.down.prev = pointer

                if direction == "LEFT":
                    testX = pointer.x-1
                    testY = pointer.y
                    pointer.left = Cell()
                    pointer.left.x = testX
                    pointer.left.y = testY
                    pointer.left.right = pointer
                    pointer.left.distance = self.CalculateDistanceToFinishline(pointer.left.x, pointer.left.y)
                    if testX >= 0:
                        pointer.left.celltype = self.board[testY][testX]
                    else:
                        pointer.left.celltype = "BORDER"
                    if pointer.left.celltype == " ":
                        if pointer.left.distance < smallest_distance:
                            if not pointer.left.blocked:
                                smallest_distance = pointer.left.distance
                                pointer.goto = pointer.left
                                pointer.left.prev = pointer

                if direction == "RIGHT":
                    testX = pointer.x+1
                    testY = pointer.y
                    pointer.right = Cell()
                    pointer.right.x = testX
                    pointer.right.y = testY
                    pointer.right.left = pointer
                    pointer.right.distance = self.CalculateDistanceToFinishline(pointer.right.x, pointer.right.y)
                    if testX < len(self.board[testY]):
                        pointer.right.celltype = self.board[testY][testX]
                    else:
                        pointer.right.celltype = "BORDER"
                    if pointer.right.celltype == " ":
                        if pointer.right.distance < smallest_distance:
                            if not pointer.right.blocked:
                                smallest_distance = pointer.right.distance
                                pointer.goto = pointer.right
                                pointer.right.prev = pointer

            # test if the maze is solved
            try:
                solved_up = self.board[pointer.up.y][pointer.up.x] == "F"
            except:
                solved_up = False
            
            try:
                solved_down = self.board[pointer.down.y][pointer.down.x] == "F"
            except:
                solved_down = False

            try:
                solved_left = self.board[pointer.left.y][pointer.left.x] == "F"
            except:
                solved_left = False

            try:
                solved_right = self.board[pointer.right.y][pointer.right.x] == "F"
            except:
                solved_right = False
            
            solved = solved_up or solved_down or solved_left or solved_right
            
            # goto next cell
            if not solved:
                if pointer.goto != None:
                    pointer = pointer.goto
                    self.board[pointer.y][pointer.x] = "U"
                else:
                    # go back
                    pointer.blocked = True
                    pointer = pointer.prev
            else:
                if solved_up:
                    pointer.goto = pointer.up
                    pointer.up.prev = pointer
                if solved_down:
                    pointer.goto = pointer.down
                    pointer.down.prev = pointer
                if solved_left:
                    pointer.goto = pointer.left
                    pointer.left.prev = pointer
                if solved_right:
                    pointer.goto = pointer.right
                    pointer.right.prev = pointer
                pointer = pointer.goto
            try:
                self.canvas.coords(self.pointer, pointer.x-4, pointer.y-4, pointer.x+4, pointer.y+4)
            except:
                pass
        
        # SAVE RESULT AS PNG FILE
        # calculate path back
        path = []
        path.append(str(pointer.x)+":"+str(pointer.y))
        while pointer.prev != None:
            pointer = pointer.prev
            path.append(str(pointer.x)+":"+str(pointer.y))
        path.append(str(pointer.x)+":"+str(pointer.y))
        
        # calculate shortcuts in the path
        largest_index = 0
        index = 0
        improved_path = []
        while index < len(path)-1:
            cell = path[index]
            index += 1

            xy = cell.split(":")
            x = int(xy[0])
            y = int(xy[1])
            
            # search for adjecent up
            adjX = x
            adjY = y-1
            point = str(adjX)+":"+str(adjY) 
            if point in path:
                i = path.index(point)
                if i > largest_index:
                    largest_index = i
                    index = largest_index
            
            # search for adjecent down
            adjX = x
            adjY = y+1
            point = str(adjX)+":"+str(adjY) 
            if point in path:
                i = path.index(point)
                if i > largest_index:
                    largest_index = i
                    index = largest_index

            # search for adjecent left
            adjX = x-1
            adjY = y
            point = str(adjX)+":"+str(adjY) 
            if point in path:
                i = path.index(point)
                if i > largest_index:
                    largest_index = i
                    index = largest_index
            
            # search for adjecent right
            adjX = x+1
            adjY = y
            point = str(adjX)+":"+str(adjY) 
            if point in path:
                i = path.index(point)
                if i > largest_index:
                    largest_index = i
                    index = largest_index
            improved_path.append(path[index])
        path = improved_path

        # reduce unnecessary turn
        index = 0
        path.reverse()
        improved_path = [path[index]]
        while index < len(path):
            start_point = path[index]
            found_shortcut = False
            start_pointXY = start_point.split(":")
            start_pointX = int(start_pointXY[0])
            start_pointY = int(start_pointXY[1])
            # input("START POINT: "+start_point) 

            # look UP
            testX = start_pointX
            testY = start_pointY-1
            cell = None
            potential_add = [start_point]
            while testY >= 0 and cell != "█":
                cell = self.board[testY][testX]
                point = str(testX)+":"+str(testY)
                potential_add.append(point)
                #input("   POINT "+point+" - "+cell)
                if point in path:
                    i = path.index(point)
                    if i > index:
                        index = i
                        if improved_path[-1] == potential_add[0]:
                            improved_path += potential_add[1:]
                        else:
                            improved_path += potential_add
                        found_shortcut = True
                        #input("   FOUND A SHORTCUT TO "+point)
                        #input(improved_path)
                        break
                testY -= 1
            
            # look DOWN
            testX = start_pointX
            testY = start_pointY+1
            cell = None
            potential_add = [start_point]
            while testY < len(self.board) and cell != "█":
                cell = self.board[testY][testX]
                point = str(testX)+":"+str(testY)
                potential_add.append(point)
                if point in path:
                    i = path.index(point)
                    if i > index:
                        index = i
                        if improved_path[-1] == potential_add[0]:
                            improved_path += potential_add[1:]
                        else:
                            improved_path += potential_add
                        found_shortcut = True
                        break
                testY += 1

            # look LEFT
            testX = start_pointX-1
            testY = start_pointY
            cell = None
            potential_add = [start_point]
            while testX >= 0 and cell != "█":
                cell = self.board[testY][testX]
                point = str(testX)+":"+str(testY)
                potential_add.append(point)
                if point in path:
                    i = path.index(point)
                    if i > index:
                        index = i
                        if improved_path[-1] == potential_add[0]:
                            improved_path += potential_add[1:]
                        else:
                            improved_path += potential_add
                        found_shortcut = True
                        break
                testX -= 1

            # look RIGHT
            testX = start_pointX+1
            testY = start_pointY
            cell = None
            potential_add = [start_point]
            while testX < len(self.board) and cell != "█":
                cell = self.board[testY][testX]
                point = str(testX)+":"+str(testY)
                potential_add.append(point)
                if point in path:
                    i = path.index(point)
                    if i > index:
                        index = i
                        #print(improved_path)
                        if improved_path[-1] == potential_add[0]:
                            improved_path += potential_add[1:]
                        else:
                            improved_path += potential_add
                        found_shortcut = True
                        break
                testX += 1
            
            # found shortcut?
            if not found_shortcut:
                index += 1
                if len(improved_path) > 0:
                    if start_point != improved_path[-1]:
                        improved_path.append(start_point)
                else:
                    improved_path.append(start_point)
                #input(improved_path)

        # save as solved.png
        display = []
        y = 0
        x = 0
        for row in self.board:
            for col in row:
                cell = col
                if self.board[y][x] != "S":
                    if str(x)+":"+str(y) in improved_path:
                        cell = "*"
                display.append(self.colors[cell])
                x += 1
            y += 1
            x = 0
        
        # generate image
        img = Image.new('RGB', (self.width, self.heigth))
        img.putdata(display)
        img.save('solved.png')
        
        # PROJECT RESULT ONTO SCREEN
        self.solvedPNG = ImageTk.PhotoImage(Image.open("solved.png"))
        self.canvas.create_image(2, 2, image=self.solvedPNG, anchor=NW)
        self.load_button.config(state=NORMAL)
    
    def CalculateDistanceToFinishline(self, x, y):
        return math.sqrt( (abs(self.finish_point[0]-x))**2 + (abs(self.finish_point[1]-y))**2 )
    
    def Exit(self):
        self.root.destroy()
        os._exit(1)
MazeSolver()
