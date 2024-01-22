import math
from PIL import Image

class MazeSolver:
    def __init__(self):
        # global vars
        self.Player = [0,0] # the x,y location of the Player
        self.Target = [0,0] # the x,y location of the Target
        self.StartPoint = [0,0] # the x,y location of the StartPoint
        self.Next = [] # a list of potential next steps a list of (delta,x,y)
        self.Board = {} # a list of Cell objects
        self.width = 0 # maze width
        self.height = 0 # maze height
        
        # start
        self.start()
    
    def start(self):
        win = False
        self.create_maze()
        while not win:
            win = True
            if self.Player[0] != self.Target[0] or self.Player[1] != self.Target[1]:
                win = False
                self.calculate_next_step()
                self.move()
        self.draw_maze()
    
    def create_maze(self):
        # load image
        img = Image.open("maze.png")
        pix = img.load()
        self.width = img.size[0]
        self.height = img.size[1]

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
                        self.Player[0] = x
                        self.Player[1] = y
                        self.StartPoint[0] = x
                        self.StartPoint[1] = y
                        startPoint = True
                
                # finish
                if not finishPoint:
                    if color[0] == 237 and color[1] == 28 and color[2] == 36:
                        obj = "F"
                        self.Target[0] = x
                        self.Target[1] = y
                        finishPoint = True
                
                # add cell to board
                loc = str(x)+":"+str(y)
                self.Board[loc] = Cell(x,y,obj)

    def move(self):
        next_cell = self.Next.pop()
        x = next_cell[1]
        y = next_cell[2]
        loc1 = str(self.Player[0])+":"+str(self.Player[1])
        loc2 = str(x)+":"+str(y)
        self.Board[loc1].obj = "*"
        self.Player[0] = x
        self.Player[1] = y
        self.Board[loc2].obj = "P"
    
    def calculate_next_step(self):
        directions = [(0,-1), (0,1), (-1,0), (1,0)]
        for cor in directions:
            x = self.Player[0]+cor[0]
            y = self.Player[1]+cor[1]
            # d=√((x_2-x_1)²+(y_2-y_1)²)
            delta = math.ceil(math.sqrt((self.Target[0]-x)**2 + (self.Target[1]-y)**2))
            loc = str(x)+":"+str(y)
            if loc in self.Board:
                if self.Board[loc].obj != "W" and self.Board[loc].obj != "P" and self.Board[loc].obj != "*":
                    self.Next.append((delta,x,y))
                    self.Board[loc].obj = "*"
        self.Next.sort(reverse=True)
    
    def draw_maze(self):
        display = []
        colors = {"W": (0,0,0), "P":(0,162,232), "F":(237,28,36), " ":(255,255,255), "*":(222, 216, 35)}
        for y in range(self.height):
            for x in range(self.width):
                loc = str(x)+":"+str(y)
                start_loc = str(self.StartPoint[0])+":"+str(self.StartPoint[1])
                end_loc = str(self.Target[0])+":"+str(self.Target[1])
                cell = self.Board[loc]
                if loc != start_loc and loc != end_loc:
                    obj = cell.obj
                else:
                    if loc == start_loc:
                        obj = "P"
                    elif loc == end_loc:
                        obj = "F"
                add = colors[obj]
                display.append(add)
        new_im = Image.new("RGB",(self.width,self.height))
        new_im.putdata(display)
        new_im.show()
        new_im.save("result.png")

class Cell:
    def __init__(self,x,y,obj):
        self.x = x
        self.y = y
        self.obj = obj

MazeSolver()