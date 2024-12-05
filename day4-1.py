# day 4-1
import numpy as np
from pathlib import Path
from icecream import ic

input = Path("day4input.txt")
# input = Path("day4inputTEST.txt")

def count_xmas(chars_4) -> int:
    # ic(chars_4)
    count = 0
    for blah in chars_4:
        for y in blah:
            test = ''.join(y)
            # print(f"{test=}")
            if test == "XMAS" or test == "SAMX":
                count += 1
    return count

def create_diagrl(data: np.ndarray) -> np.ndarray:
    diag_rl: list[list[int]] = [data.diagonal(i).tolist() for i in range(-data.shape[0]+1, data.shape[1])]
    biggest = max([len(d) for d in diag_rl])
    for x in diag_rl:
        x.extend(['.']*(biggest-len(x)))
    return np.array(diag_rl)

def create_diaglr(data: np.ndarray) -> np.ndarray:
    diag_rl: list[list[int]] = [np.fliplr(data).diagonal(i).tolist() for i in range(-data.shape[0]+1, data.shape[1])]
    biggest = max([len(d) for d in diag_rl])
    for x in diag_rl:
        x.extend(['.']*(biggest-len(x)))
    return np.array(diag_rl)
    

def create_views(data: np.ndarray):
    total = 0
    
    # horizontal - do nothing
    horiz = np.lib.stride_tricks.sliding_window_view(data, 4, 1)
    # ic(data)
    total += count_xmas(horiz)
    
    # vertical
    vert = np.lib.stride_tricks.sliding_window_view(data, 4, 0)
    total += count_xmas(vert)

    # diagonal lr
    # diag_rl = [data.diagonal(i).tolist() for i in range(-data.shape[0]+1, data.shape[1])]
    diag_rl = create_diagrl(data)
    # ic(diag_rl)
    total += count_xmas(np.lib.stride_tricks.sliding_window_view(diag_rl, 4, 1))
    
    # diagonal rl
    diag_lr = create_diaglr(data)
    total += count_xmas(np.lib.stride_tricks.sliding_window_view(diag_lr, 4, 1))
    
    return total

def create_array():
    with input.open() as f:
        lines = f.readlines()

    cleaned=[]    
    for line in lines:
        cleaned.append(list(line.strip()))
        
    return np.array(cleaned)
        
def main():
    data = create_array()
    total = create_views(data)
    print(f"{total=}")


if __name__ == "__main__":
    main()