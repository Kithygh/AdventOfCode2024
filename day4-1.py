# day 4-1
import numpy as np
from pathlib import Path
from icecream import ic

input = Path("day4input.txt")
# input = Path("day4inputTEST.txt")

def count_xmas(windows) -> int:
    # ic(chars_4)
    count = 0
    for blah in windows:
        for row in blah:
            test = ''.join(row)
            # print(f"{test=}")
            if test == "XMAS" or test == "SAMX":
                count += 1
    return count

def create_diag_view(data:np.ndarray) -> np.ndarray:
    diags: list[list[int]] = [data.diagonal(i).tolist() for i in range(-data.shape[0]+1, data.shape[1])]
    longest = max([len(d) for d in diags])
    for x in diags:
        x.extend(['.']*(longest-len(x)))
    return np.array(diags)   

def create_window_views(data: np.ndarray):
    # horizontal - do nothing
    yield np.lib.stride_tricks.sliding_window_view(data, 4, 1)
    
    # vertical - use different axis for sliding window
    yield np.lib.stride_tricks.sliding_window_view(data, 4, 0)

    # diagonal lr
    diag_rl = create_diag_view(data)
    yield np.lib.stride_tricks.sliding_window_view(diag_rl, 4, 1)
    
    # diagonal rl
    diag_lr = create_diag_view(np.fliplr(data))
    yield np.lib.stride_tricks.sliding_window_view(diag_lr, 4, 1)
    

def get_lines():
    with input.open() as f:
        return f.readlines()

def create_array(raw_data: list[str]):
    cleaned=[]    
    for line in raw_data:
        cleaned.append(list(line.strip()))
    return np.array(cleaned)
        
def main():
    raw_data = get_lines()
    data = create_array(raw_data)
    total = 0
    for view in create_window_views(data):
        total += count_xmas(view)
    print(f"{total=}")


if __name__ == "__main__":
    main()