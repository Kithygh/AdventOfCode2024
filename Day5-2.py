# day 5-2

from pathlib import Path
from icecream import ic

input = Path("day5input.txt")
# input = Path("day5inputTEST.txt")

def test_rules(rules):
    for rule in rules:
        assert len(rule) == 2
def test_editions(editions):
    for update in editions:
        assert len(update) % 2 == 1

def get_lines():
    with input.open() as f:
        return f.readlines()

def gather_rules_and_editions():
    rules = []
    editions = []
    for line in get_lines():
        if line == '\n':
            continue
        if '|' in line:
            rules.append(line.strip().split(sep='|'))
        else:
            editions.append(line.strip().split(sep=','))

    return rules, editions

def verify_update(update: list, rules):
    for rule in rules:
        try:
            if update.index(rule[0]) < update.index(rule[1]):
                continue
            else:
                return False
        except ValueError:
            continue
    return True

def get_rejected_editions(editions, rules):
    rejected_editions = []
    for update in editions:
        if not verify_update(update, rules):
            rejected_editions.append(update)
    return rejected_editions

def assemble_master_rule(rules):
    master = []
    def recursion(rules):
        if len(rules) == 1: # base case
            master.extend(rules[0])
            return master
        # find what left number isn't on right
        next_to_add = [r[0] for r in rules if r[0] not in {r[1] for r in rules}][0]
        # add that number to master
        master.append(next_to_add)
        # remove rules that start with that number
        rules = [r for r in rules if r[0] != next_to_add]
        # call recursion
        return recursion(rules)
    return recursion(rules)

def narrow_down_rules(edition, rules):
    ed_rules = [r for r in rules if r[0] in edition and r[1] in edition]
    return ed_rules

def center_sum(editions):
    return sum([int(e[int((len(e)-1)/2)]) for e in editions])

def main():
    rules, editions = gather_rules_and_editions()
    test_rules(rules)
    test_editions(editions)
    total = 0

    rejected_editions = get_rejected_editions(editions, rules)

    fixed_editions = []
    for e in rejected_editions:
        fixed = []
        narrowed_rules = narrow_down_rules(e, rules)
        master_rule = assemble_master_rule(narrowed_rules)
        for x in master_rule:
            if x in e:
                fixed.append(x)
        fixed_editions.append(fixed)

    total = center_sum(fixed_editions)
    ic(total)

if __name__ == "__main__":
    main()
