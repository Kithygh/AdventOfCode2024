# day 8-1
from icecream import ic
from pathlib import Path
import numpy as np
from itertools import pairwise, product, combinations
from functools import lru_cache

input = Path("day8input.txt")
# input = Path("day8inputTEST.txt")

def get_lines():
    with input.open() as f:
        data = f.readlines()
    return data

def get_grid():
    ar = [list(line.strip()) for line in get_lines()]
    return np.array(ar)

def in_bounds(coord, grid: np.ndarray) -> bool:
    if coord[0] < 0 or coord[0] > grid.shape[0]-1:
        return False
    if coord[1] < 0 or coord[1] > grid.shape[1]-1:
        return False
    return True

def extract_freqs(grid: np.ndarray) -> list[str]:
    return np.delete(np.unique_counts(grid)[0], 0).tolist()

@lru_cache
def combos(antenna_count: int):
    return list(combinations(list(range(antenna_count)),2))

def calculate_antinodes(antenna_pairs):
    antinodes = set()
    for coord in antenna_pairs:
        ydiff = coord[1][0] - coord[0][0]
        xdiff = coord[1][1] - coord[0][1]
        antinode1 = coord[1][0] + ydiff, coord[1][1] + xdiff
        antinode2 = coord[0][0] - ydiff, coord[0][1] - xdiff
        antinodes.add(antinode1)
        antinodes.add(antinode2)
    return antinodes

def validate_antinodes(antinodes, grid: np.ndarray):
    return [a for a in antinodes if in_bounds(a, grid)]

def main():
    grid = get_grid()
    freqs = extract_freqs(grid)
    # ic(freqs)
    total_an = set()
    for freq in freqs:
        # ic(freq)
        antennas = np.where(grid == freq)
        # ic(antennas)
        pairs = combos(len(antennas[0]))
        # ic(pairs)
        antenna_pairs = [((antennas[0][p[0]],antennas[1][p[0]]), (antennas[0][p[1]], antennas[1][p[1]])) for p in pairs]
        # ic(antenna_pairs)
        antinodes = calculate_antinodes(antenna_pairs)
        # ic(antinodes)
        antinodes = validate_antinodes(antinodes, grid)
        # ic(antinodes)
        total_an.update(antinodes)
    # ic(total_an)
    ic(len(total_an))

if __name__ == "__main__":
    main()
