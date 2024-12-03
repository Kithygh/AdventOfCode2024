# day 3-1
from pathlib import Path
import re

input = Path("day3input.txt")
# input = Path("day3inputTEST.txt")

def get_muls(line: str) -> list[str]:
    muls = re.findall("mul\([0-9]{1,3},[0-9]{1,3}\)", line)
    return muls

def mul_result(mul: str) -> int:
    mul = mul[4:-1]
    a, b = mul.split(',')
    return int(a) * int(b)

total = 0
with input.open() as data:
    for line in data:
        muls = get_muls(line)
        for mul in muls:
            total += mul_result(mul)
print(total)