# day 15-1
from icecream import ic
# import icecream
from pathlib import Path
import numpy as np
from dataclasses import dataclass
from itertools import chain
import pprint

# preferredWidth = 1000
# pp = pprint.PrettyPrinter(width=preferredWidth)
# ic.configureOutput(argToStringFunction=pp.pformat)
# ic.lineWrapWidth = preferredWidth

np.set_printoptions(linewidth=1000)


@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError
        return Point(self.x + other.x, self.y + other.y)

@dataclass
class Crate:
    location: Point

    def can_move(self, direction):
        if direction == Dir.L or direction == Dir.R:
            spot_to_move = self.location + direction
            return grid[*spot_to_move] == '.'

        if direction == Dir.U or direction == Dir.D:
            spot1 = self.location + direction
            spot2 = self.location + direction + Dir.R
            return grid[*spot1] == '.' and grid[*spot2] == '.'

TEST = True
grid: np.ndarray = None
moves = []

@dataclass
class Dir:
    U = (-1, 0)
    D = ( 1, 0)
    L = ( 0,-1)
    R = ( 0, 1)

def parse_map():
    global grid
    map_file = Path.cwd() / "inputs" / f"day15map{'TEST' if TEST else ''}.txt"
    with map_file.open() as f:
        data = f.readlines()
    grid = np.array([[x for x in row]
                    for row
                    in [list(line.strip()) for line in data]])

def expanded_map():
    global grid
    map_file = Path.cwd() / "inputs" / f"day15map{'TEST' if TEST else ''}.txt"
    with map_file.open() as f:
        data = f.readlines()

    arrays = [list(line.strip()) for line in data]
    ic(arrays)
    new_arrays = []
    for a in arrays:
        new_line = []
        for char in a:
            new_line.extend(widening(char))
        new_arrays.append(new_line)
    grid = np.array([[x for x in row]
                    for row
                    in new_arrays])

def widening(char) -> list[str, str]:
    if char == '#':
        return ['#', '#']
    if char == 'O':
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

def move_robot(robot, direction):
    old_loc = robot

    free_space = find_stopping_point(robot, direction)
    if free_space is not None:
        grid[*free_space] = 'O' # fill the free space
        grid[*np.add(robot, direction)] = '@' # move robot
        grid[*old_loc] = '.' # leave free space behind

def find_stopping_point(robot, direction):
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
    boxes = np.argwhere(grid == 'O')
    return sum([100*box[0] + box[1] for box in boxes])


def main():
    # parse_map()
    expanded_map()
    
    ic(grid)
    exit()
    parse_moves()
    robot = find_robot()

    for direction in moves:
        move_robot(robot, direction)
        robot = find_robot()

    print(calculate_GPS())

if __name__ == "__main__":
    main()
