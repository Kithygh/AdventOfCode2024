# day 14-1
from icecream import ic
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize, linewidth=350)


fileinput = Path.cwd() / "inputs" / "day14input.txt"
# fileinput = Path.cwd() / "inputs" / "day14inputTEST.txt"

@dataclass
class Point:
    x: int
    y: int


@dataclass
class Robot:
    loc: Point
    x_vel: int
    y_vel: int

    def advance(self, seconds):
        self.loc.x = (self.loc.x + (self.x_vel * seconds)) % grid.shape[0]
        self.loc.y = (self.loc.y + (self.y_vel * seconds)) % grid.shape[1]
        # self.loc = Point(end_x, end_y)

robots: list[Robot] = []
grid: np.ndarray

def get_lines():
    with fileinput.open() as f:
        data = f.readlines()
    return data

def parse_robots():
    data = get_lines()
    for line in data:
        blah = line.split()
        x_start, y_start = blah[0].split(',')
        x_start = int(x_start[2:])
        y_start = int(y_start)
        x_vel, y_vel = blah[1].split(',')
        x_vel = int(x_vel[2:])
        y_vel = int(y_vel)
        robots.append(Robot(Point(x_start, y_start), x_vel, y_vel))

def place_robots():
    for robot in robots:
        grid[robot.loc.x, robot.loc.y] += 1

def get_quadrants():
    half_x = int(grid.shape[0] / 2)
    half_y = int(grid.shape[1] / 2)
    q1 = grid[:half_x, :half_y]
    q2 = grid[half_x+1:, :half_y]
    q3 = grid[:half_x, half_y+1:]
    q4 = grid[half_x+1:, half_y+1:]
    return [q1,q2,q3,q4]

def measure_quadrants():
    blah = []
    for q in get_quadrants():
        blah.append(sum(sum(q)))
    return blah

def display_grid():
    for x in grid:
        for y in x:
            if y == 0:
                print(' ', end='')
            else:
                print('X', end='')
        print('\n')

def main():
    global grid
    # grid = np.zeros((11,7), int)
    grid = np.zeros((101,103), int)

    parse_robots()
    seconds = 0
    while True:
        grid[:] = 0
        for robot in robots:
            robot.advance(1)
        place_robots()
        seconds += 1
        display_grid()
        x = input(f"current seconds {seconds}")
        if x != '':
            break
    # ic(robots)
    # print(grid)
    # ic(grid)
    quads = measure_quadrants()
    # ic(quads)
    safety_factor = 1
    for q in quads:
        safety_factor *= q
    ic(safety_factor)
        

if __name__ == "__main__":
    main()
