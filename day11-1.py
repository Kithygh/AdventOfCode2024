# day 11-1
from icecream import ic
from pathlib import Path
from functools import lru_cache
from collections import namedtuple

input = Path("day11input.txt")
# input = Path("day11inputTEST.txt")

def get_lines():
    with input.open() as f:
        return f.readline()

def read_stones():
    nums = [n for n in get_lines().split()]
    stones = [Stone(int(n), 0) for n in nums]
    return stones

# had to be a named tuple and not a dataclass as it needs to be hashable for the lru_cache
Stone = namedtuple('Stone', ['value', 'blink_count'])

@lru_cache
def alter_stone(stone: Stone) -> list[Stone]:
    next_count = stone.blink_count+1

    """If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1."""
    if stone.value == 0:
        return [Stone(1, stone.blink_count+1)]

    """If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    The left half of the digits are engraved on the new left stone, and the right half of
    the digits are engraved on the new right stone.
    (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)"""
    stringed = str(stone.value)
    if len(stringed) % 2 == 0:
        half = int(len(stringed)/2)
        stone1 = Stone(int(stringed[:half]), next_count)
        stone2 = Stone(int(stringed[half:]), next_count)
        return [stone1, stone2]

    """If none of the other rules apply, the stone is replaced by a new stone; 
    the old stone's number multiplied by 2024 is engraved on the new stone."""
    return [Stone(2024*stone.value, next_count), ]


def main():
    total = 0
    stones = read_stones()
    ic(stones)
    while stones:

        # grab a stone
        stone = stones.pop()

        # if that stone is done blinking, remove and increment total
        if stone.blink_count == 25:
            total += 1
            continue

        # otherwise lets feed it to the machine and append the result back onto the stack
        stones.extend(alter_stone(stone))
    ic(total)

if __name__ == "__main__":
    main()
