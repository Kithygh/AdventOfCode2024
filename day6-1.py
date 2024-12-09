# day 6-1
from pathlib import Path
from icecream import ic
import numpy as np

input = Path("day6input.txt")
# input = Path("day6inputTEST.txt")
guard: np.ndarray
direction = [-1,0]
grid: np.ndarray
done = None
def get_lines():
    with input.open() as f:
        return f.readlines()

def get_grid():
    global grid
    base_array = []
    for line in get_lines():
        base_array.append([x for x in line.strip()])

    grid = np.array(base_array)

def find_guard_start():
    global guard
    global grid
    thing = np.where(grid == '^')
    guard = np.array([int(thing[0]), int(thing[1])])

def rotate_guard():
    global direction
    if direction == [-1,0]:
        direction = [0,1]; return
    if direction == [0,1]:
        direction = [1,0]; return
    if direction == [1,0]:
        direction = [0,-1]; return
    if direction == [0,-1]:
        direction = [-1,0]; return
    ic("PANIC!", direction)

def in_bounds(guard):
    if guard[0] < 0:
        return False
    if guard[0] > grid.shape[0]-1:
        return False
    if guard[1] < 0:
        return False
    if guard[1] > grid.shape[1]-1:
        return False
    return True


def move_guard():
    global grid
    global guard
    global direction
    global done
    proposed_location = guard+direction
    try:
        if grid[*proposed_location] == '#':
            rotate_guard()
        else:
            grid[*guard] = 'x'
            guard = proposed_location
    except IndexError:
        grid[*guard] = 'x'
        done = np.sum(np.char.count(grid,'x'))


def main():
    get_grid()
    find_guard_start()
    while not done:
        move_guard()
    ic(done)
if __name__ == "__main__":
    main()
