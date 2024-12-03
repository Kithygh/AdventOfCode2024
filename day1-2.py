# day 1-2
from pathlib import Path
input = Path("day1input.txt")
# input = Path("day1inputTEST.txt")
left = []
right = {}

with input.open() as data:
    for line in data:
        thing = line.split()
        left.append(int(thing[0]))
        rnum = int(thing[1])
        right[rnum] = right.get(rnum, 0) + 1

total = 0
for l in left:
    total += l * right.get(l,0)
print(total)