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
        self.Width = 0 # maze Width
        self.Height = 0 # maze Height
        self.Path = [] # the list of steps as a list of (turning direction , number of steps)
        self.Direction = "U" # can be a value U D L R
        
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
        self.draw_path()
        self.draw_maze()
    
    def create_maze(self):
        # load image
        img = Image.open("maze.png")
        pix = img.load()
        self.Width = img.size[0]
        self.Height = img.size[1]

        # convert image to list
        startPoint = False
        finishPoint = False
        for y in range(self.Height):
            #old_display = display
            for x in range(self.Width):
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
        # get the next location to be
        next_cell = self.Next.pop()
        x = next_cell[1]
        y = next_cell[2]
        old_xy = (self.Player[0], self.Player[1])
        loc1 = str(self.Player[0])+":"+str(self.Player[1])
        loc2 = str(x)+":"+str(y)

        # mark where player was so they wont be able to get back there
        self.Board[loc1].obj = "*"

        # get new x, y
        self.Player[0] = x
        self.Player[1] = y

        # update the board
        self.Board[loc2].obj = "P"

        # calculate if direction have been changed or if the player is stuck
        new_xy = (self.Player[0], self.Player[1])
        old_direction = self.Direction
        if new_xy[0] == old_xy[0]:
            if new_xy[1] > old_xy[1]:
                self.Direction = "D"
            elif new_xy[1] < old_xy[1]:
                self.Direction = "U"
        else:
            if new_xy[0] > old_xy[0]:
                self.Direction = "R"
            elif new_xy[0] < old_xy[0]:
                self.Direction = "L"

        delta = int(math.sqrt((new_xy[0]-old_xy[0])**2 + (new_xy[1]-old_xy[1])**2))
        print(old_xy, new_xy, self.Direction, delta)
        input(">")
        if delta == 1:
            pass
            #self.Path.append(self.Direction)
        self.Path.append(self.Direction)

    def calculate_next_step(self):
        directions = [(0,-1), (0,1), (-1,0), (1,0)]
        for cor in directions:
            x = self.Player[0]+cor[0]
            y = self.Player[1]+cor[1]
            # d=√((x_2-x_1)²+(y_2-y_1)²)
            delta = int(math.sqrt((self.Target[0]-x)**2 + (self.Target[1]-y)**2))
            loc = str(x)+":"+str(y)
            if loc in self.Board:
                if self.Board[loc].obj != "W" and self.Board[loc].obj != "P" and self.Board[loc].obj != "*":
                    self.Next.append((delta,x,y))
                    self.Board[loc].obj = "*"
        self.Next.sort(reverse=True)
    
    def draw_path(self):
        ghost = [0,0]
        ghost[0] = self.StartPoint[0]
        ghost[1] = self.StartPoint[1]
        for next in self.Path:
            if next == "U":
                ghost[1] -= 1
            elif next == "D":
                ghost[1] += 1
            elif next == "L":
                ghost[0] -= 1
            elif next == "R":
                ghost[0] += 1
            loc = str(ghost[0])+":"+str(ghost[1])
            if loc in self.Board:
                self.Board[loc].obj = "G"

    def draw_maze(self):
        display = []
        colors = {"W": (0,0,0), "P":(0,162,232), "F":(237,28,36), " ":(255,255,255), "*":(222, 216, 35), "G":(177, 79, 179)}
        for y in range(self.Height):
            for x in range(self.Width):
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
        new_im = Image.new("RGB",(self.Width,self.Height))
        new_im.putdata(display)
        new_im.show()
        new_im.save("result.png")

class Cell:
    def __init__(self,x,y,obj):
        self.x = x
        self.y = y
        self.obj = obj

MazeSolver()