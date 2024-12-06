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

def repair_update(update: list, rules):

    for rule in rules:
        try:
            a = update.index(rule[0])
            b = update.index(rule[1])
            if b > a:
                update[a], update[b] = update[b], update[a]
        except ValueError:
            continue
    result = verify_update(update, rules)
    if not result:
        ic("broken repair", update)
        raise
    return update


def assemble_master_rule(rules):
    master = []
    def recursion(rules):
        print("------------")
        ic(rules)
        ic(len(rules))
        if len(rules) == 1: # base case
            master.extend(rules[0])
            return master
        # find what left number isn't on right
        next_to_add = {r[0] for r in rules if r[0] not in {r[1] for r in rules}}
        ic(next_to_add)
        # next_to_add = [r[0] for r in rules if r[0] not in [r[1] for r in rules]][0]
        # add that number to master
        num_to_add = next_to_add.pop()
        master.append(num_to_add)
        # remove rules that start with that number
        rules = [r for r in rules if r[0] != num_to_add]
        # call recursion
        return recursion(rules)
    return recursion(rules)

def narrow_down_rules(edition, rules):
    ed_rules = [r for r in rules if r[0] in edition and r[1] in edition]
    return ed_rules
    

def main():
    rules, editions = gather_rules_and_editions()
    test_rules(rules)
    test_editions(editions)
    total = 0
    

    
    
    # master_rule = assemble_master_rule(rules)
    # ic(master_rule)
    rejected_editions = get_rejected_editions(editions, rules)

    fixed_editions = []
    for e in rejected_editions:
        fixed = []
        narrowed_rules = narrow_down_rules(e, rules)
        ic(len(narrowed_rules))
        # exit()
        master_rule = assemble_master_rule(narrowed_rules)
        ic(master_rule)
        for x in master_rule:
            if x in e:
                fixed.append(x)
        fixed_editions.append(fixed)
    ic(fixed_editions)

    for update in fixed_editions:
        if verify_update(update, rules):
            total += int(update[int((len(update)-1)/2)])
    # for u in rejected_editions:
    #     ic(u, "before")
    #     repair_update(u, rules)
    #     if not verify_update(u, rules):
    #         ic(u, "after")
    # for update in rejected_editions:
    #     total += int(update[int((len(update)-1)/2)])



    ic(total)

if __name__ == "__main__":
    main()
