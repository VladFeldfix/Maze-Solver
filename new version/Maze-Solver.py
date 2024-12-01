from PIL import Image
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
        # setup global vars
        self.board = []
        self.start_point = ()
        self.finish_point = ()
        self.pointer = Cell()

        # actions
        self.build_maze()
        self.solve()
    
    def build_maze(self):
        # load image
        img = Image.open('maze.png')
        pix = img.load()

        # get width and height
        self.width = img.size[0]
        self.heigth = img.size[1]
        self.smallest_distance = math.sqrt(self.width**2+self.heigth**2)   
        for y in range(self.heigth):
            # add row to board
            self.board.append([])

            for x in range(self.width):
                # determine the nature of the cell 
                # < E empty > 
                # < S start >
                # < F finish >
                # < W wall >

                cell = '_'
                value = pix[x,y]
                red = value[0]
                green = value[1]
                blue = value[2]

                # start point
                if red == 255 and green == 0 and blue == 0:
                    cell = 'S'
                    self.start_point = (x,y)
                
                # finish point
                if red == 0 and green == 0 and blue == 255:
                    cell = 'F'
                    self.finish_point = (x,y)
                
                # wall
                if cell == '_':
                    if red < 255/2:
                        cell = '█'

                # add cell to board
                self.board[y].append(cell)
        #self.display()
    
    def solve(self):
        # goto start point
        self.pointer = Cell()
        self.pointer.x = self.start_point[0]
        self.pointer.y = self.start_point[1]
        self.pointer.distance = self.calculate_distance_to_finish(self.pointer.x, self.pointer.y)
        self.pointer.celltype = "START"

        # start solving loop
        solved = False
        while not solved:
            # reset
            smallest_distance = self.smallest_distance
            self.pointer.goto = None

            # create 4 directions
            directions = ("UP", "DOWN", "LEFT", "RIGHT")
            for dir in directions:
                if dir == "UP":
                    testX = self.pointer.x
                    testY = self.pointer.y-1
                    self.pointer.up = Cell()
                    self.pointer.up.x = testX
                    self.pointer.up.y = testY
                    self.pointer.up.down = self.pointer
                    self.pointer.up.distance = self.calculate_distance_to_finish(self.pointer.up.x, self.pointer.up.y)
                    if testY >= 0:
                        self.pointer.up.celltype = self.board[testY][testX]
                    else:
                        self.pointer.up.celltype = "BORDER"
                    if self.pointer.up.celltype == "_":
                        if self.pointer.up.distance < smallest_distance:
                            if not self.pointer.up.blocked:
                                self.pointer.goto = self.pointer.up
                                self.pointer.up.prev = self.pointer

                if dir == "DOWN":
                    testX = self.pointer.x
                    testY = self.pointer.y+1
                    self.pointer.down = Cell()
                    self.pointer.down.x = testX
                    self.pointer.down.y = testY
                    self.pointer.down.up = self.pointer
                    self.pointer.down.distance = self.calculate_distance_to_finish(self.pointer.down.x, self.pointer.down.y)
                    if testY < len(self.board):
                        self.pointer.down.celltype = self.board[testY][testX]
                    else:
                        self.pointer.down.celltype = "BORDER"
                    if self.pointer.down.celltype == "_":
                        if self.pointer.down.distance < smallest_distance:
                            if not self.pointer.down.blocked:
                                self.pointer.goto = self.pointer.down
                                self.pointer.down.prev = self.pointer
                if dir == "LEFT":
                    testX = self.pointer.x-1
                    testY = self.pointer.y
                    self.pointer.left = Cell()
                    self.pointer.left.x = testX
                    self.pointer.left.y = testY
                    self.pointer.left.right = self.pointer
                    self.pointer.left.distance = self.calculate_distance_to_finish(self.pointer.left.x, self.pointer.left.y)
                    if testX >= 0:
                        self.pointer.left.celltype = self.board[testY][testX]
                    else:
                        self.pointer.left.celltype = "BORDER"
                    if self.pointer.left.celltype == "_":
                        if self.pointer.left.distance < smallest_distance:
                            if not self.pointer.left.blocked:
                                self.pointer.goto = self.pointer.left
                                self.pointer.left.prev = self.pointer
                if dir == "RIGHT":
                    testX = self.pointer.x+1
                    testY = self.pointer.y
                    self.pointer.right = Cell()
                    self.pointer.right.x = testX
                    self.pointer.right.y = testY
                    self.pointer.right.left = self.pointer
                    self.pointer.right.distance = self.calculate_distance_to_finish(self.pointer.right.x, self.pointer.right.y)
                    if testX < len(self.board[testY]):
                        self.pointer.right.celltype = self.board[testY][testX]
                    else:
                        self.pointer.right.celltype = "BORDER"
                    if self.pointer.right.celltype == "_":
                        if self.pointer.right.distance < smallest_distance:
                            if not self.pointer.right.blocked:
                                self.pointer.goto = self.pointer.right
                                self.pointer.right.prev = self.pointer
                
            # solved
            solved = self.board[self.pointer.up.y][self.pointer.up.x] == "F" or self.board[self.pointer.down.y][self.pointer.down.x] == "F" or self.board[self.pointer.left.y][self.pointer.left.x] == "F" or self.board[self.pointer.right.y][self.pointer.right.x] == "F"

            # goto next place
            if not solved:
                if self.pointer.goto != None:
                    self.pointer = self.pointer.goto
                    self.board[self.pointer.y][self.pointer.x] = "U"
                else:
                    self.pointer.blocked = True
                    self.pointer = self.pointer.prev
                # show result
                self.display()
            else:
                print("SOLVED")
                self.display_solution()
    
    def calculate_distance_to_finish(self, x, y):
        deltax = abs(self.finish_point[0]-x)
        deltay = abs(self.finish_point[1]-y)
        return math.sqrt(deltax**2+deltay**2)

    def display(self):
        display = ""
        y = 0
        x = 0
        for row in self.board:
            for col in row:
                if self.pointer.x == x and self.pointer.y == y:
                    display += "*"
                else:
                    display += col
                x += 1
            display += "\n"
            y += 1
            x = 0
        print(display)
        """
        print("Pointer:")

        print('self.pointer.up: ',self.pointer.up)
        print('self.pointer.down: ',self.pointer.down)
        print('self.pointer.left: ',self.pointer.left)
        print('self.pointer.right: ',self.pointer.right)
        print('self.pointer.x: ',self.pointer.x)
        print('self.pointer.y: ',self.pointer.y)
        print('self.pointer.distance: ',self.pointer.distance)
        print('self.pointer.celltype: ',self.pointer.celltype)
        print('self.pointer.goto: ',self.pointer.goto)
        print('self.pointer.prev: ',self.pointer.prev)
        print('self.pointer.blocked: ',self.pointer.blocked)
        """
        #input(">")
    
    def display_solution(self):
        pointer = self.pointer
        path = []
        path.append(str(pointer.x)+":"+str(pointer.y))
        while pointer.prev != None:
            pointer = pointer.prev
            path.append(str(pointer.x)+":"+str(pointer.y))
        display = ""
        y = 0
        x = 0
        for row in self.board:
            for col in row:
                if col == "U" or col == "_":
                    col = " "
                if str(x)+":"+str(y) in path:
                    display += "*"
                else:
                    display += col
                x += 1
            display += "\n"
            y += 1
            x = 0    
        print(display)
MazeSolver()