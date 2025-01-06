# day 15-1
from queue import Queue
from icecream import ic
# import icecream
from pathlib import Path
import numpy as np
from dataclasses import dataclass
from itertools import chain
from typing import Self
import os
import time
# preferredWidth = 1000
# pp = pprint.PrettyPrinter(width=preferredWidth)
# ic.configureOutput(argToStringFunction=pp.pformat)
# ic.lineWrapWidth = preferredWidth

np.set_printoptions(linewidth=1000)

@dataclass
class Dir:
    U = (-1, 0)
    D = ( 1, 0)
    L = ( 0,-1)
    R = ( 0, 1)

@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self):
        return (self.x, self.y)

    def __add__(self, other: Self):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple) and len(other) == 2:
            return Point(self.x + other[0], self.y + other[1])

    def __iter__(self):
        return iter((self.x, self.y))

@dataclass
class Crate:
    location: Point

    def __key(self):
        # ic(self.location)
        return (self.location.x, self.location.y)
    def __hash__(self):
        return hash(self.__key())

    def __init__(self, arr: np.ndarray):
        x = arr.x
        y = arr.y
        self.location = Point(x,y)

    def can_move(self, direction: Dir):
        if direction == Dir.L or direction == Dir.R:
            spot_to_move = self.location + direction
            return grid[*spot_to_move] == '.'

        if direction == Dir.U or direction == Dir.D:
            spot1 = self.location + direction
            spot2 = self.location + direction + Dir.R
            return grid[*spot1] == '.' and grid[*spot2] == '.'

    def move_crate(self, direction: Dir):

        grid[*(self.location + direction)] = '['
        grid[*(self.location + direction + Dir.R)] = ']'
    def erase_crate(self):
        grid[*self.location] = '.'
        grid[*self.location+ Dir.R] = '.'

    def find_blocking_crates(self, direction: Dir) -> list[Self]:
        """ Returns False if there is a wall in the way
            Returns with an empty list if there is nothing in the way
            Returns a list of crate(s) if there are crates in the way"""
        # if there is nothing in the way, blocking crates is empty
        if self.can_move(direction):
            return []

        if direction == Dir.L:
            spot_to_move = self.location + direction
            if grid[*spot_to_move] == '#':
                return False
            if grid[*spot_to_move] == ']':
                return [Crate(spot_to_move + Dir.L), ]
            return [] # else theres nothing in the way

        if direction == Dir.R:
            spot_to_move = self.location + direction + direction
            if grid[*spot_to_move] == '#':
                return False
            if grid[*spot_to_move] == '[':
                return [Crate(spot_to_move)]
            return [] # else theres nothing in the way

        if direction == Dir.U or direction == Dir.D:
            if grid[*(self.location + direction)] == '#':
                return False
            if grid[*(self.location + direction + Dir.R)] == '#':
                return False
            crates = []
            if grid[*(self.location + direction)] == '[': # directly vertical
                crates.append(Crate(self.location + direction))
            if grid[*(self.location + direction)] == ']': # vertical left
                crates.append(Crate(self.location + direction + Dir.L))
            if grid[*(self.location + direction + Dir.R)] == '[': # vertical right
                crates.append(Crate(self.location + direction + Dir.R))
            return crates
        ic("{")
        ic(direction)
        ic("}")
TEST = False
grid: np.ndarray = None
moves: list[Dir] = []
box_count: int = 0

def expanded_map():
    global grid
    map_file = Path.cwd() / "inputs" / f"day15map{'TEST' if TEST else ''}.txt"
    with map_file.open() as f:
        data = f.readlines()

    arrays = [list(line.strip()) for line in data]

    new_arrays = [chain.from_iterable(map(widen, a))
                  for a
                  in arrays]

    grid = np.array([[x for x in row]
                    for row
                    in new_arrays])

def widen(char: str) -> list[str, str]:
    global box_count
    if char == '#':
        return ['#', '#']
    if char == 'O':
        box_count += 1
        return ['[', ']']
    if char == '.':
        return ['.', '.']
    if char == '@':
        return ['@', '.']
    raise ValueError

def parse_moves():
    global moves
    moves_file = Path.cwd() / "inputs" / f"day15moves{'TEST' if TEST else ''}.txt"
    with moves_file.open() as f:
        data = f.readlines()
    chars = [x for x in chain.from_iterable(line.strip() for line in data)]
    for char in chars:
        match char:
            case '^':
                moves.append(Dir.U)
            case '>':
                moves.append(Dir.R)
            case 'v':
                moves.append(Dir.D)
            case '<':
                moves.append(Dir.L)

def move_robot(robot: np.ndarray, direction: Dir):
    old_loc = robot
    spot_to_look = Point(*(np.add(robot, direction)))
    char = grid[*spot_to_look]

    # If it's a wall, we're done
    if char == '#':
        return
    # If it's open space, move in and we're done
    if char == '.':
        grid[*spot_to_look] = '@'
        grid[*old_loc] = '.'
        return

    # Otherwise we have a crate in our direction.
    if char == '[':
        crate = Crate(spot_to_look)
    if char == ']':
        crate = Crate(spot_to_look + Dir.L)



    crates_to_move = find_crates(crate, direction)
    if crates_to_move is not None:
        # If we have a list of crates, move them
        for crate in crates_to_move:
            crate.erase_crate()
        for crate in crates_to_move:
            crate.move_crate(direction)
        # then move the robot
        grid[*spot_to_look] = '@'
        grid[*old_loc] = '.'
        # grid[*free_space] = 'O' # fill the free space
        # grid[*np.add(robot, direction)] = '@' # move robot
        # grid[*old_loc] = '.' # leave free space behind

def find_crates(crate: Crate, direction: Dir) -> set[Crate]:
    frontier: Queue[Crate] = Queue()
    frontier.put(crate)

    reached: set[Crate] = set()
    reached.add(crate)


    while not frontier.empty():
        current = frontier.get()
        more_crates = current.find_blocking_crates(direction)
        if more_crates == False: # False = can't move, we're done looking
            return None
        # if len(more_crates) == 0:
        #     continue
        if more_crates is None:
            ic(grid)
            ic(frontier)
            ic(reached)
            ic(current)
        for next in more_crates:
            if next not in reached:
                frontier.put(next)
                reached.add(next)
    return reached




def find_stopping_point(robot: np.ndarray, direction: Dir):
    loop_count = 1
    while True:
        robot_offset = tuple(map(lambda x: x * loop_count, direction))
        current = np.add(robot, robot_offset)
        char = grid[*current]
        if char == 'O':
            # keep looking
            loop_count += 1
            continue
        if char == '.':
            # we can move
            return current
        if char == '#':
            # hit a wall, can't move
            return None
        raise TypeError # make sure we don't see any other characters

def find_robot() -> Point:
    return np.argwhere(grid == '@')[0]

def calculate_GPS():
    boxes = np.argwhere(grid == '[')
    return sum([100*box[0] + box[1] for box in boxes])

def verify_box_count():
    if len(np.argwhere(grid == '[')) == box_count:
        return
    ic(grid)
    raise AssertionError

def main():
    expanded_map()
    ic(grid)

    parse_moves()
    robot = find_robot()
    # print(type(robot))
    # exit()
    for direction in moves:
        # ic(grid)
        # ic(direction)
        move_robot(robot, direction)
        verify_box_count()
        robot = find_robot()
        # time.sleep(1)
        # os.system('cls')
    ic(grid)

    print(calculate_GPS())

if __name__ == "__main__":
    main()
