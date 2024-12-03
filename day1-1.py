# day 1

from pathlib import Path
input = Path("day1input.txt")
left = []
right = []

with input.open() as data:
    for line in data:
        thing = line.split()
        left.append(int(thing[0]))
        right.append(int(thing[1]))
left = sorted(left)
right = sorted(right)

total = 0
for l,r in zip(left, right):
    total += abs(l-r)
print(total)