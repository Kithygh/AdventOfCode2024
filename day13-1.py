# day 13-1

from pathlib import Path
import numpy as np
from dataclasses import dataclass
from icecream import ic
# from collections import namedtuple

input = Path.cwd() / "inputs" / "day13input.txt"
# input = Path.cwd() / "inputs" / "day13inputTEST.txt"



@dataclass
class Button:
    x: int
    y: int

@dataclass
class Goal:
    x: int
    y: int

@dataclass
class ClawMachine:
    a: Button
    b: Button
    goal: Goal
    a_presses: int = 0
    b_presses: int = 0

    def token_cost(self):
        if self.a_presses:
            return 3 * self.a_presses + self.b_presses
        return 0

machines: list[ClawMachine] = []

def get_lines():
    with input.open() as f:
        data = f.readlines()
    return data

def parse_claw_machines():
    data = get_lines()
    for line in data:
        n = line.split()
        if not n:
            continue
        if n[1] == 'A:':
            buttona = Button(int(n[2][2:-1]), int(n[3][2:]))
        if n[1] == 'B:':
            buttonb = Button(int(n[2][2:-1]), int(n[3][2:]))
        if n[0] == 'Prize:':
            goal = Goal(int(n[1][2:-1]), int(n[2][2:]))
            machines.append(ClawMachine(buttona, buttonb, goal))

def test_machine(claw: ClawMachine):
    while claw.b_presses * claw.b.x < claw.goal.x:
        claw.b_presses += 1
        x = claw.b_presses * claw.b.x
        y = claw.b_presses * claw.b.y
        # test if x is even reachable by a presses
        if (claw.goal.x - x) % claw.a.x == 0:
            multa_x = int((claw.goal.x - x) / claw.a.x)
            if (claw.goal.y - y) == claw.a.y * multa_x:
                claw.a_presses = multa_x
                return
    claw.b_presses = None
    claw.a_presses = None

def main():
    parse_claw_machines()
    for machine in machines:
        test_machine(machine)
    token_cost = 0
    # for machine in machines:
    #     token_cost += machine.token_cost()
        
    token_cost = sum(m.token_cost() for m in machines)
    ic(token_cost)

if __name__ == "__main__":
    main()
