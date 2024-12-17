# day 11-2
from icecream import ic
from pathlib import Path
from functools import lru_cache

input = Path("day11input.txt")
# input = Path("day11inputTEST.txt")

def get_lines():
    with input.open() as f:
        return f.readline()

def read_stones():
    nums = [n for n in get_lines().split()]
    stones = [int(n) for n in nums]
    return stones

@lru_cache
def alter_stone(value: int) -> list[int]:

    """If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1."""
    if value == 0:
        return [1,]

    """If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    The left half of the digits are engraved on the new left stone, and the right half of
    the digits are engraved on the new right stone.
    (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)"""
    stringed = str(value)
    if len(stringed) % 2 == 0:
        half = int(len(stringed)/2)
        stone1 = int(stringed[:half])
        stone2 = int(stringed[half:])
        return [stone1, stone2]

    """If none of the other rules apply, the stone is replaced by a new stone;
    the old stone's number multiplied by 2024 is engraved on the new stone."""
    return [2024*value, ]

def stones_to_buckets(stones: list[int]):
    buckets = {}
    for stone in stones:
        buckets[stone] = buckets.get(stone, 0) + 1
    return buckets

def main():
    total = 0
    stones = read_stones()
    buckets = stones_to_buckets(stones)
    num_blinks = 75
    new_buckets = {}
    for _ in range(num_blinks):
        new_buckets = {}
        for stone, count in buckets.items():
            for r in alter_stone(stone):
                new_buckets[r] = new_buckets.get(r, 0) + count
        buckets = new_buckets.copy()

    total = sum(buckets.values())
    ic(total)

if __name__ == "__main__":
    main()
