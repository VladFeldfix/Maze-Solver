from PIL import Image

class MazeSolver:
    def __init__(self):
        self.start()
    
    def start(self):
        # setup global vars
        self.BOARD = []
        self.player = Player(0,0)
        self.target = [1,1]

        # play
        self.create_maze()
        win = False
        while not win:
            win = True
            if self.player.x != self.target[0] or self.player.y != self.target[1]:
                win = False
                # create next step cells
                # evaluate the distance of each next cell
                # move to the lowest distance cell
                # make this cell blocket so it cannot be reused
        # now there is a tree of all paths player took, cut down all the unused branches
    
    def create_maze(self):
        # load image
        im = Image.open('maze.jpg')
        pix = im.load()
        width = im.size[0]
        height = im.size[1]

        # convert image to list
        display = ""
        startPoint = None
        finishPoint = None
        for y in range(height):
            for x in range(width):
                color = pix[x,y]
                wall = False
                addToDisplay = "  "
                
                # wall
                if color[0] == 0 and color[1] == 0 and color[2] == 0:
                    wall = True
                    addToDisplay = "[]"
                
                # start
                if startPoint == None:
                    if color[0] == 0 and color[1] == 162 and color[2] == 232:
                        wall = True
                        addToDisplay = ":)"
                        startPoint = (x,y)
                
                # finish
                if finishPoint == None:
                    if color[0] == 237 and color[1] == 28 and color[2] == 36:
                        wall = True
                        addToDisplay = "$$"
                        finishPoint = (x,y)
                
                # add cell to board
                self.BOARD.append((x,y,Floor(x,y,wall)))
                display += addToDisplay
            display += "\n"
        print(display)

class Floor:
    def __init__(self,x,y,wall):
        self.x = x
        self.y = y
        self.wall = wall

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

MazeSolver()