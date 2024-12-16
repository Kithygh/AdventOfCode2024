# day 10-1
from icecream import ic
from pathlib import Path
import numpy as np
from itertools import repeat

input = Path("day10input.txt")
# input = Path("day10inputTEST.txt")

def get_lines():
    with input.open() as f:
        data = f.readlines()
    return data

def get_grid():
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
    def recursion(coords: list[tuple[int, int]]):
        target = grid[coords[0][0], coords[0][1]] + 1
        if target == 10:
            return coords

        neighbors = []
        for coord in coords:
            neighbors.extend(find_neighbors(coord, grid))
        blah = [(neighbor[0],neighbor[1])
                for neighbor in neighbors
                if grid[neighbor[0],neighbor[1]] == target]
        return recursion(list(blah))
    return recursion([coord,])

def find_trailheads(grid: np.ndarray):
    ar = np.where(grid == 0)
    return list(zip(ar[0], ar[1]))

def main():
    grid = get_grid()
    trailheads = find_trailheads(grid)
    total = 0
    for trailhead in trailheads:
    # for x,y in zip(trailheads[0], trailheads[1]):
        total += len(find_trailends(trailhead, grid))
    ic(total)

if __name__ == "__main__":
    main()
