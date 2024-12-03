# day 2-2
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
            return try_harder(report)
    return True

def is_safe2(report: list[int]) -> bool:
    if report[0] > report[-1]:
        report = list(reversed(report))
    for a,b in itertools.pairwise(report):
        diff = b - a
        if diff > 3 or diff < 1:
            return False
    return True

def try_harder(report: list[int]) -> bool:
    for x in range(len(report)):
        cut_report = report.copy()
        cut_report.pop(x)
        if is_safe2(cut_report):
            return True
    return False
            
    
total = 0
with input.open() as data:
    for line in data:
        report = list(map(int, line.split()))
        total += is_safe(report)

print(total)
