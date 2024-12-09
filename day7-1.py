# day 7-1
from icecream import ic
from pathlib import Path
from itertools import permutations, combinations_with_replacement, product
from datetime import datetime

input = Path("day7input.txt")
# input = Path("day7inputTEST.txt")

class Equation:
    def __init__(self, total: int, numbers: list[int]):
        self.total = total
        self.numbers = numbers
        self.valid = False

    def create_eval_strings(nums) -> str:
        eval_strings = []
        ops = "+*"
        length = len(nums) - 1 # take that, fencepost error!

        for seq in list(product(ops, repeat=length)):
            s = '(' * len(seq) + str(nums[0])
            for op, n in zip(seq, nums[1:]):
                s += op + str(n) + ')'
            eval_strings.append(s)
        return eval_strings

    def check_valid(self):
        seqs = Equation.create_eval_strings(self.numbers)
        for seq in seqs:
            if eval(seq) == self.total:
                self.valid = True
                return

    def __str__(self): # for print
        return f"total: {self.total}, numbers: {[x for x in self.numbers]}"
    def __repr__(self): # for icecream
        return f"total: {self.total}, numbers: {[x for x in self.numbers]}"

def get_lines():
    with input.open() as f:
        data = f.readlines()
    return data

def parse_eqs(lines: list[str]) -> list[Equation]:
    eqs = []
    for line in lines:
        total = int(line.split(sep=':')[0])
        nums = [int(x) for x in line.split(sep=':')[1].split()]
        eqs.append(Equation(total, nums))
    return eqs

def main():
    ic(datetime.now().isoformat(), "start")
    lines = get_lines()
    eqs = parse_eqs(lines)
    for eq in eqs:
        eq.check_valid()
    valid = [x for x in eqs if x.valid]
    invalid = [x for x in eqs if not x.valid]
    total = sum([x.total for x in valid])
    ic(f"{total=}")
    ic(datetime.now().isoformat(), "done")

if __name__ == "__main__":
    main()
