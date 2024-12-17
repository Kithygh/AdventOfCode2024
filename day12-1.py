# day 12-1
from queue import Queue
from icecream import ic
from pathlib import Path
import numpy as np
from collections import namedtuple
from itertools import product
from dataclasses import dataclass
from queue import Queue

input = Path.cwd() / "inputs" /"day12input.txt"
input = Path.cwd() / "inputs" /"day12inputTEST.txt"



Point = namedtuple('Point', ['x','y'])

@dataclass
class Region:
    label: str
    members: list[Point]
    perimeter: int = 0

grid: np.ndarray = None
regions: list[Region] = []

def get_lines():
    with input.open() as f:
        return f.readlines()

def get_grid():
    global grid
    base_array = []
    for line in get_lines():
        base_array.append([x for x in line.strip()])

    grid = np.array(base_array)



def in_bounds(coord: Point) -> bool:
    if coord.x < 0 or coord.x > grid.shape[0]-1:
        return False
    if coord.y < 0 or coord.y > grid.shape[1]-1:
        return False
    return True

def find_neighbors(coord: Point):
    # get a coord
    neighbors = []
    orthos = [Point(0,1), Point(1,0), Point(0,-1), Point(-1,0)]
    # check the 4 cardinal directions
    for dir in orthos:
        modified_coord = Point(coord.x + dir.x, coord.y + dir.y)
        # if in bounds, add to list
        if in_bounds(modified_coord):
            neighbors.append(modified_coord)
    return neighbors

def in_region(coord: Point) -> bool:
    # if coord is already included in a region, return True
    for region in regions:
        if coord in region.members:
            return True
    return False

def find_region(coord: Point):
    frontier = Queue()
    frontier.put(coord)
    reached = set()
    reached.add(coord)
    label = grid[coord]
    region = Region(label, [coord, ])
    
    while not frontier.empty():
        current = frontier.get()
        ic(current)
        for next in find_neighbors(current):
            if next not in reached and grid[next] == label:
                ic(next)
                frontier.put(next)
                reached.add(next)
                region.members.append(next)
    ic(region)
    ic(len(region.members))

# def find_region(coord: Point):
#     label = grid[coord]
#     region = Region(label, [coord, ])
#     # while True:
#     #     neighbors = find_neighbors(coord)
#     #     neighbors = [n for n in neighbors if grid[n] == label]
#     #     region.members.extend(neighbors)
#     def recursion(coords: list[Point]):
#         neighbors = find_neighbors(coord)
#         region_members = [n for n in neighbors if grid[n] == label]
#         region.perimeter += 4 - len(region_members)
#         if not region_members:
#             return
#         region.members.extend(neighbors)
        
        
            
def main():
    get_grid()
    # for coord in product(range(grid.shape[0]), range(grid.shape[1])):
    #     ic(coord)
    for coord in np.ndindex(grid.shape):
        coord = Point(*coord)
        if not in_region(coord):
            find_region(coord)
            exit()
    pass

if __name__ == "__main__":
    main()
