# day 5-1

from pathlib import Path
from icecream import ic

input = Path("day5input.txt")
# input = Path("day5inputTEST.txt")

def test_rules(rules):
    for rule in rules:
        assert len(rule) == 2
def test_updates(updates):
    for update in updates:
        assert len(update) % 2 == 1

def get_lines():
    with input.open() as f:
        return f.readlines()

def gather_rules_and_updates():
    rules = []
    updates = []
    for line in get_lines():
        if line == '\n':
            continue
        if '|' in line:
            rules.append(line.strip().split(sep='|'))
        else:
            updates.append(line.strip().split(sep=','))

    return rules, updates

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

def main():
    rules, updates = gather_rules_and_updates()
    test_rules(rules)
    test_updates(updates)
    total = 0
    for update in updates:
        if verify_update(update, rules):
            total += int(update[int((len(update)-1)/2)])
    ic(total)

if __name__ == "__main__":
    main()
