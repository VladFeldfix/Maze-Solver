import math
from PIL import Image

class maze_solver:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.Player = [0,0] # the x,y location of the Player
        self.Target = [0,0] # the x,y location of the Target
        self.StartPoint = [0,0] # the x,y location of the StartPoint
        self.Next = [] # a list of potential next steps a list of (delta,x,y)
        self.Board = {} # a list of Cell objects
        self.Width = 0 # maze Width
        self.Height = 0 # maze Height
        self.Path = [] # a linked list of step objects Step(x,y,Next) where next is a Step object too

    def create_maze(self, fileLocation):
        # load image
        img = Image.open(fileLocation)
        pix = img.load()
        self.Width = img.size[0]
        self.Height = img.size[1]

        # error maze too big
        if self.Width > 500 or self.Height > 500:
            return (False, "This file is too big. Max size is 500x500")
    
        # convert image to list
        startPoint = False
        finishPoint = False
        for y in range(self.Height):
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
        
        # return evaluation result
        if not startPoint:
            return (False, "This file has no start point! To make a start point color at leat one pixel RBG (0,162,232)")
        if not finishPoint:
            return (False, "This file has no finish point! To make a finish point color at leat one pixel RBG (237,28,36)")
        
        # if everything is ok
        return (True, "")
    
    def calculate_next_step(self):
        directions = [(0,-1), (0,1), (-1,0), (1,0)]
        for cor in directions:
            x = self.Player[0]+cor[0]
            y = self.Player[1]+cor[1]
            # d=√((x_2-x_1)²+(y_2-y_1)²)
            delta1 = int(math.sqrt((self.Target[0]-x)**2 + (self.Target[1]-y)**2))
            delta2 = int(math.sqrt((self.Player[0]-x)**2 + (self.Player[1]-y)**2))
            score = delta1+delta2
            loc = str(x)+":"+str(y)
            if loc in self.Board:
                if self.Board[loc].obj != "W" and self.Board[loc].obj != "P" and self.Board[loc].obj != "*":
                    self.Next.append((score,x,y))
                    self.Board[loc].obj = "*"
        self.Next.sort(reverse=True)  
    
    def move(self):
        # get the next location to be
        next_cell = self.Next.pop()
        x = next_cell[1]
        y = next_cell[2]
        loc1 = str(self.Player[0])+":"+str(self.Player[1])
        loc2 = str(x)+":"+str(y)

        # mark where player was so they wont be able to get back there
        self.Board[loc1].obj = "*"

        # get new x, y
        self.Player[0] = x
        self.Player[1] = y

        # update the board
        self.Board[loc2].obj = "P"

    def add_step(self, x,y, Win):
        # insert a new point to the list
        new_step = Step(x, y, None, [], Win)
        self.Path.append(new_step)

        # search for adjacent point to make a link
        for step in self.Path:
            if step.x == new_step.x or step.y == new_step.y:
                if (step.x - new_step.x)**2 == 1 or (step.y - new_step.y)**2 == 1:
                    step.Next.append(new_step)
                    new_step.Prev = step

    def draw_path(self):
        # select win step
        winning_step = None
        for step in self.Path:
            if step.Win:
                winning_step = step
        pointer = winning_step

        # search for the first point
        path = []
        while pointer.Prev != None:
            path.append(pointer)
            pointer = pointer.Prev
        
        for step in path:
            loc = str(step.x)+":"+str(step.y)
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
        #new_im.show()
        new_im.save("result.png")
   
class Cell:
    def __init__(self,x,y,obj):
        self.x = x
        self.y = y
        self.obj = obj

class Step:
    def __init__(self,x,y,Prev,Next,Win):
        self.x = x
        self.y = y
        self.Prev = Prev
        self.Next = Next
        self.Win = Win