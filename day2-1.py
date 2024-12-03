# day 2
from pathlib import Path
import itertools

input = Path("day2input.txt")
# input = Path("day2inputTEST.txt")

def is_safe(report: list[int]) -> bool:
    if report[0] > report[-1]:
        report = list(reversed(report))
    for a,b in itertools.pairwise(report):
        diff = b - a
        if diff > 3 or diff < 1:
            return False
    return True
    
total = 0
with input.open() as data:
    for line in data:
        report = list(map(int, line.split()))
        total += is_safe(report)

print(total)
