from queue import PriorityQueue
from visualization import *
import pygame

def heuristic(point1:tuple,point2:tuple,type="man"):
    """
        Calculates the h cost for A* either using Manhattan ("man") Distance (defualt)
        or Euclidian ("euc") distance between two points of form (x,y) 
    """
    x1, y1 = point1
    x2, y2 = point2
    
    delta_y = abs(y1 - y2)
    delta_x = abs(x1 - x2)

    if type == "man":
        return delta_y + delta_x
    elif type == "euc":
        rad = delta_y**2 + delta_x**2
        return pow(rad,0.5)
    

def reconstruct_path(came_from, current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end, h_type="man"):
    count = 0
    # Creating our open set. Using Priority Queue
    open_set = PriorityQueue()
    open_set.put((0,count,start)) # (f_score, count, cell)

    came_from = {} # keeps track of where the next cell came from

    # Setting the g score for all points in the grid to infinity first
    g_score = {cell: float("inf") for row in grid for cell in row}
    # Setting the g score for the start point to be 0, since we are already on the start
    g_score[start] = 0
    # setting the f score for all points in the grid to infinity first
    f_score = {cell: float("inf") for row in grid for cell in row}
    # f score for start is just the h score
    f_score[start] = heuristic(start.get_pos(),end.get_pos(),h_type)
    # Priority Queue can't tell me what is inside. Using this to keep track of the cells in the open set
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current_cell = open_set.get()[2] # grabbing the lowest value f score
        open_set_hash.remove(current_cell)

        if current_cell == end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True
        for neighbor in current_cell.neighbors:
            temp_g_score = g_score[current_cell] + 1 # cost to move to the next neighbor is 1 (no diags)
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_cell
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(),end.get_pos(),h_type)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current_cell != start:
            current_cell.make_closed()
        
    return False