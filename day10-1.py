# day 10-1
from icecream import ic
from pathlib import Path
import numpy as np

input = Path("day10input.txt")
# input = Path("day10inputTEST.txt")

def get_lines():
    with input.open() as f:
        data = f.readlines()
    return data

def get_grid():
    # ar = [list(line.strip()) for line in get_lines()]
    # return np.array([[int(x) for x in y] for y in ar])
    return np.array([[int(x) for x in row]
                     for row
                     in [list(line.strip()) for line in get_lines()]])

def in_bounds(coord, grid: np.ndarray) -> bool:
    if coord[0] < 0 or coord[0] > grid.shape[0]-1:
        return False
    if coord[1] < 0 or coord[1] > grid.shape[1]-1:
        return False
    return True

def find_neighbors(coord: tuple[int,int], grid: np.ndarray):
    # get a coord
    cons = []
    dirs = [(0,1), (1,0), (0,-1), (-1,0)]
    # check the 4 cardinal directions
    for dir in dirs:
        modified_coord = (coord[0]+dir[0], coord[1]+dir[1])
        # if in bounds, add to list
        if in_bounds(modified_coord, grid):
            cons.append(modified_coord)
    return cons

def find_trailends(coord: tuple[int, int], grid: np.ndarray) -> np.ndarray:
    # ic(coord)
    # trailends = []
    def recursion(coords: list[tuple[int, int]]):
        # ic(coords)
        target = grid[coords[0][0], coords[0][1]] + 1
        if target == 10:
            return coords

        neighbors = [find_neighbors(coord, grid) for coord in coords]
        blah = set()
        for neighbor in neighbors:
            # ic(neighbor)
            for x,y in neighbor:
                # ic(neighbor)
                if grid[x,y] == target:
                    blah.add((x,y))
        return recursion(list(blah))
    return recursion([coord,])

# def find_next_step(coords: np.ndarray, grid: np.ndarray) -> np.ndarray:
#     target = grid[coords[0][0], coords[1][0]] + 1
#     next_steps: list[list[int], list[int]] = [[],[]]
#     neighbors = []
#     blah = set()
#     for i in range(len(coords[0])):
#         neighbors.append(find_neighbors((coords[0][i], coords[1][i]), grid))
#     for neighbor in neighbors:
#         # ic(neighbor)
#         for x,y in neighbor:
#             if grid[x,y] == target:
#                 blah.add((x,y))
#                 # next_steps[0].append(x)
#                 # next_steps[1].append(y)
#     next_steps_x = [x[0] for x in blah]
#     next_steps_y = [y[1] for y in blah]
#     return [next_steps_x, next_steps_y]
    

def find_trailheads(grid: np.ndarray):
    return np.where(grid == 0)

def main():
    grid = get_grid()
    # ic(grid)
    trailheads = find_trailheads(grid)
    ic(trailheads)
    # trailheads = [[0,],[2]]
    ic(trailheads)
    # exit()
    total = 0
    for x,y in zip(trailheads[0], trailheads[1]):
        thing = find_trailends((x,y), grid)
        # ic(thing)
        # ic(len(thing))
        total += len(thing)
    ic(total)
    
if __name__ == "__main__":
    main()
