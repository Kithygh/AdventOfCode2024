# day 7-1
from icecream import ic
from pathlib import Path
from itertools import permutations, combinations_with_replacement, product
from datetime import datetime

input = Path("day7input.txt")
input = Path("day7inputTEST.txt")

class Equation:
    def __init__(self, total: int, numbers: list[int]):
        self.total = total
        self.numbers = numbers
        self.valid = False

    def create_eval_strings(nums) -> str:
        eval_strings = []
        ops = "+* "
        length = len(nums) - 1 # take that, fencepost error!
        op_sequences = list(product(ops, repeat=length))
        # ic(op_sequences)
        op_sequences = [''.join(x) for x in op_sequences]
        # ic(op_sequences)
        for seq in op_sequences:
            leading_paren_count = len(seq) - seq.count(' ')
            s = '(' * leading_paren_count + str(nums[0])
            for op, n in zip(seq, nums[1:]):
                # ic(s)
                if op == ' ':
                    s += str(n)
                else:
                    s += ')' + op + str(n)
            eval_strings.append(s)
        return eval_strings

    def check_valid(self):
        seqs = Equation.create_eval_strings(self.numbers)
        for seq in seqs:
            if eval(seq) == self.total:
                self.valid = True
                return

    def __str__(self): # for print
        return f"valid: {self.valid:2} total: {self.total:15}, numbers: {[x for x in self.numbers]}"
    def __repr__(self): # for icecream
        return f"valid: {self.valid:2} total: {self.total:15}, numbers: {[x for x in self.numbers]}"

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
    total = sum([x.total for x in valid])
    for eq in eqs:
        ic(eq)
    ic(f"{total=}")
    ic(datetime.now().isoformat(), "done")

if __name__ == "__main__":
    main()
