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
        self.Path = None # a linked list of step objects Step(x,y,Next) where next is a Step object too
        
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
        loc1 = str(self.Player[0])+":"+str(self.Player[1])
        loc2 = str(x)+":"+str(y)

        # mark where player was so they wont be able to get back there
        self.Board[loc1].obj = "*"

        # get new x, y
        self.Player[0] = x
        self.Player[1] = y

        # update the board
        self.Board[loc2].obj = "P"

        # make a journy diary
        self.add_step(self.Player[0],self.Player[1])
        """
        # get the new location
        new_xy = (self.Player[0], self.Player[1])
        # write down what direction player went to
        direction = "X"
        if new_xy[0] == old_xy[0]:
            if new_xy[1] > old_xy[1]:
                direction = "D"
            elif new_xy[1] < old_xy[1]:
                direction = "U"
        else:
            if new_xy[0] > old_xy[0]:
                direction = "R"
            elif new_xy[0] < old_xy[0]:
                direction = "L"
        # white down the last location and what direction should be taken from there
        self.Path.append([old_xy,direction])
        #print(old_xy,direction)
        # the distance between the last and this xy to see if there was a leap
        delta = int(math.sqrt((new_xy[0]-old_xy[0])**2 + (new_xy[1]-old_xy[1])**2))
        # if there was a leap mark this place with an x
        if delta > 1:
            self.Path[-1][1] = "X"


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
        self.Path.append([old_xy, True])
        if delta != 1:
            i = 0
            for x in self.Path:
                self.Path[i][1] = True
                i += 1
            print("Before: ",self.Path)
            adjacent = False
            i = len(self.Path)-1
            while not adjacent:
                p1 = new_xy
                p2 = self.Path[i][0]
                adjacent = self.test_adjacent(p1, p2)
                print(p1,p2,adjacent)
                if not adjacent:
                    self.Path[i][1] = False
                i -= 1
            print("After:  ",self.Path)
        """
        #input(">")
    """
    def test_adjacent(self, point1, point2):
        result = False
        if (point1[0] - point2[0])**2 == 1 and point1[1] - point2[1] == 0:
            result = True
        elif (point1[1] - point2[1])**2 == 1 and point1[0] - point2[0] == 0:
            result = True
        return result
    """
    def add_step(self, x,y):
        # first step
        if self.Path == None:
            self.Path = Step(x, y, None, None)
            self.pointer = self.Path
        else:
            # see if the new step is adjacent to the last step
            adjacent = False
            if x == self.pointer.x or y == self.pointer.y:
                adjacent = True

            if adjacent:
                self.pointer.Next = Step(x, y, None, self.pointer)
                self.pointer = self.pointer.Next
            else:
                tmp = self.pointer
                while not adjacent:
                    tmp = tmp.Prev
                    if x == tmp.x or y == tmp.y:
                        adjacent = True
                self.pointer = tmp
                self.pointer.Next = Step(x, y, None, self.pointer)
                self.pointer = self.pointer.Next

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
        print(self.Path)
        ghost = [0,0]
        """
        for step in self.Path:
            if step[1]:
                ghost = step[0]
                loc = str(ghost[0])+":"+str(ghost[1])
                if loc in self.Board:
                    self.Board[loc].obj = "G"
        
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
        """
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

class Step:
    def __init__(self,x,y,Next,Prev):
        self.x = x
        self.y = y
        self.Next = Next
        self.Prev = Prev
MazeSolver()