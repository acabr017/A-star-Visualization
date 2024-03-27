import pygame
from astar import *


# Setting up the Game Window



# Setting up the Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQ = (64,224,208)


class Cell: 

    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.colour = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    

    def is_closed(self):
        return self.colour == RED
    

    def is_open(self):
        return self.colour == GREEN
    

    def is_barrier(self):
        return self.colour == BLACK
    

    def is_start(self):
        return self.colour == ORANGE
    

    def is_end(self):
        return self.colour == TURQ
    

    def reset(self):
        self.colour = WHITE

    
    def make_closed(self):
        self.colour = RED
    

    def make_open(self):
        self.colour = GREEN


    def make_barrier(self):
        self.colour = BLACK


    def make_start(self):
        self.colour = ORANGE
    

    def make_end(self):
        self.colour = TURQ
    

    def make_path(self):
        self.colour = PURPLE


    def draw(self,win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))


    def update_neighbors(self,grid):
        self.neighbors = []
        # Checking down
        if self.row < self.total_rows - 1 and not grid[self.row +1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Checking Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Checking Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Checking Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self,other):
        return False
    


def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i,j, gap, rows)
            grid[i].append(cell)
    
    return grid
    

def draw_grid(win, rows, width):
    gap  = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(width=1000,ROWS=50, h_type="man"):
    WIN = pygame.display.set_mode((width,width))
    pygame.display.set_caption("A* Visualization")
    grid = make_grid(ROWS,width)

    start = None
    end = None

    run = True
    started = False # this will be deleted

    while run:
        draw(WIN,grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                # This is the left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,ROWS,width)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell # TODO: Simplify this
                    start.make_start()
                
                elif not end and cell != start:
                    end = cell # TODO: Simplify this
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_barrier()
                    

            elif pygame.mouse.get_pressed()[2]:
                # This is the right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,ROWS,width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    
                    algorithm(lambda: draw(WIN, grid, ROWS, width), grid, start, end,h_type)
                
                if event.key == pygame.K_c:
                    # clear the screen
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)
    pygame.quit()