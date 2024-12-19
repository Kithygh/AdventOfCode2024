# day 12-1
from queue import Queue
from icecream import ic
from pathlib import Path
import numpy as np
from datetime import datetime
from dataclasses import dataclass
from queue import Queue

input = Path.cwd() / "inputs" /"day12input.txt"
# input = Path.cwd() / "inputs" /"day12inputTEST.txt"

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError
        return Point(self.x + other.x, self.y + other.y)\

    def __key(self):
        return (self.x, self.y)
    def __hash__(self):
        return hash(self.__key())

    def to_tuple(self):
        return (self.x, self.y)

@dataclass
class Region:
    label: str
    members: list[Point]
    perimeter: int = 0

    def __repr__(self):
        return f"Label: {self.label}, Member count: {len(self.members)}, Perimeter: {self.perimeter}"

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

def find_neighbors(coord: Point) -> list[Point]:
    # get a coord
    neighbors = []
    orthos = [Point(0,1), Point(1,0), Point(0,-1), Point(-1,0)]
    # check the 4 cardinal directions
    for dir in orthos:
        modified_coord = coord + dir
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

def find_region(coord: Point) -> None:
    frontier = Queue()
    frontier.put(coord)
    reached = set()
    reached.add(coord.to_tuple())
    label = grid[coord.to_tuple()]
    region = Region(label, [])

    while not frontier.empty():
        current = frontier.get()
        for next in find_neighbors(current):
            if next not in reached:
                reached.add(next)
                if grid[next.to_tuple()] == label:
                    region.members.append(next)
                    frontier.put(next)
    if not region.members:
        region.members.append(coord)

    regions.append(region)

def is_corner(string: str) -> bool:
    return {'000': True,
             '001': False,
             '010': True,
             '011': False,
             '100': False,
             '101': True,
             '110': False,
             '111': False,
             }[string]

def measure_perimeter2(region: Region) -> None:
    for plot in region.members:
        neighbors = find_corners(plot)
        for corners in neighbors:
            string = ""
            for c in corners:
                if not in_bounds(c):
                    string += '0'
                else:
                    string += '1' if grid[c.to_tuple()] == region.label else '0'
            region.perimeter += is_corner(string)


def find_corners(coord: Point) -> list[list[Point, Point, Point]]:
    UR = [coord + Point(0, 1), coord + Point( 1, 1), coord + Point( 1, 0)]
    LR = [coord + Point(1, 0), coord + Point( 1,-1), coord + Point( 0,-1)]
    LL = [coord + Point(0,-1), coord + Point(-1,-1), coord + Point(-1, 0)]
    UL = [coord + Point(-1,0), coord + Point(-1, 1), coord + Point( 0, 1)]
    return [UR, LR, LL, UL]

def main():
    get_grid()
    print(datetime.now(), "Starting region defining")
    # Defining regions
    for coord in np.ndindex(grid.shape):
        coord = Point(*coord)
        if not in_region(coord):
            find_region(coord)

    print(datetime.now(), "Starting perimeter calculation")
    # Calculating region perimeter
    for r in regions:
        measure_perimeter2(r)

    print(datetime.now(), "Starting price calculation")
    # Calculate fencing price
    total = sum([len(r.members) * r.perimeter for r in regions])
    ic(total)
    print(datetime.now(), "Complete")

if __name__ == "__main__":
    main()
