# day 3-2
from pathlib import Path
import re

input = Path("day3input.txt")
# input = Path("day3inputTEST.txt")

enable = True

def get_commands(line: str) -> list[str]:
    commands = re.findall("mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)", line)
    return commands

def command_result(command: str) -> int:
    global enable
    if command.startswith("mul"):
        if enable:
            a, b = command[4:-1].split(',')
            return int(a) * int(b)
    else:
        enable = False if command == "don't()" else True
    return 0
        

total = 0
with input.open() as data:
    for line in data:
        commands = get_commands(line)
        for command in commands:
            total += command_result(command)
print(total)