# day 4-2
import numpy as np
from pathlib import Path
from icecream import ic

input = Path("day4input.txt")
# input = Path("day4inputTEST.txt")

def get_lines():
    with input.open() as f:
        return f.readlines()

def char_to_int(x):
    match x:
        case 'M':
            return 1
        case 'S':
            return 2
        case 'A':
            return 10
        case _:
            return 20

def check_for_X(sub_grid):
    if sub_grid[1,1] != 10:
        return 0
    if (sub_grid[(0,0)] + sub_grid[(2,2)] == 3) and (sub_grid[(0,2)] + sub_grid[(2,0)] == 3):
        return 1
    return 0

def create_array(raw_data: list[str]) -> np.ndarray:
    cleaned=[]
    for line in raw_data:
        cleaned.append([char_to_int(x) for x in list(line.strip())])
    return np.array(cleaned)

def main():
    raw_data = get_lines()
    data = create_array(raw_data)
    total = 0
    for i in range(1, data.shape[0]-1):
        for j in range(1, data.shape[1]-1):
            sub_grid = data[i-1:i+2, j-1:j+2]
            total += check_for_X(sub_grid)
    ic(total)

if __name__ == "__main__":
    main()
