# day 16-1
from queue import Queue
from icecream import ic
# import icecream
from pathlib import Path
import numpy as np
from dataclasses import dataclass
from itertools import chain
from typing import Self
import sys

TEST = False
grid: np.ndarray = None
np.set_printoptions(threshold=sys.maxsize)

@dataclass
class Dir:
    N = (-1, 0)
    S = ( 1, 0)
    W = ( 0,-1)
    E = ( 0, 1)

    def opposite(self) -> Self:
        if self == Dir.N:
            return Dir.S
        if self == Dir.S:
            return Dir.N
        if self == Dir.W:
            return Dir.E
        if self == Dir.E:
            return Dir.W

@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self):
        return (self.x, self.y)

    def __add__(self, other: Self) -> Self:
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple) and len(other) == 2:
            return Point(self.x + other[0], self.y + other[1])

#     def __iter__(self):
#         return iter((self.x, self.y))

@dataclass
class Loc:
    p: Point
    d: Dir

    def __key(self):
        # ic(self.location)
        return (self.p.x, self.p.y, self.d)
    def __hash__(self):
        return hash(self.__key())

def parse_map():
    global grid
    maze_file = Path.cwd() / "inputs" / f"day16input{'TEST' if TEST else ''}.txt"
    with maze_file.open() as f:
        data = f.readlines()
    grid = np.array([[x for x in row]
                    for row
                    in [list(line.strip()) for line in data]])

def find_reindeer() -> tuple[int,int]:
    location = np.argwhere(grid == 'S')[0]
    # ic(location)
    return Point(int(location[0]), int(location[1]))
def find_end() -> tuple[int,int]:
    location = np.argwhere(grid == 'E')[0]
    # ic(location)
    return Point(int(location[0]), int(location[1]))

def find_exit():
    return np.argwhere(grid == 'E')[0]


def find_moves(loc: tuple[Loc, int]) -> dict[Loc: int]:
    # ic(loc)
    orig_cost = loc[1]
    loc: Loc = loc[0]
    moves: dict[Loc: int] = {}
    dirs: list[Dir] = [Dir.N, Dir.E, Dir.S, Dir.W]
    dirs.remove(Dir.opposite(loc.d)) # don't try to go backwards
    for dir in dirs:
        pos: Point = loc.p + dir
        if grid[pos.to_tuple()] != '#':
            # ic(pos)
            cost = 1
            if loc.d != dir: # If we have to turn, add 1000 for the turn
                cost += 1000
            moves[Loc(pos, dir)] = cost + orig_cost
    return moves

def find_paths(reindeer):
    start = Loc(reindeer, Dir.E)
    frontier: Queue[(Loc,int)] = Queue()

    frontier.put((start, 0))

    reached: dict[Loc: int] = {start: 0}

    while not frontier.empty():
        current = frontier.get()
        possible_moves = find_moves(current)
        for loc, cost in possible_moves.items():
            if loc not in reached:
                reached[loc] = cost
                frontier.put((loc,cost))
            else:
                if reached[loc] > cost:
                    reached[loc] = cost
                    frontier.put((loc,cost))
    return reached


def grid_print():
    print('\n'.join(''.join(str(cell) for cell in row) for row in grid))

def main():
    parse_map()
    grid_print()
    reindeer = find_reindeer()
    end = find_end()
    ic(reindeer)
    paths = find_paths(reindeer)
    dests = {path: cost for path, cost in paths.items() if path.p == end}
    ic(dests)

if __name__ == "__main__":
    main()
