# day 5-2

from pathlib import Path
from icecream import ic

input = Path("day5input.txt")
input = Path("day5inputTEST.txt")

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

def get_rejected_updates(updates, rules):
    rejected_updates = []
    for update in updates:
        if not verify_update(update, rules):
            rejected_updates.append(update)
    return rejected_updates

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
        if len(rules) == 1:
            ic(master)
            master.append(rules[0][0])
            master.append(rules[0][1])
            return master
        
        # find what left number isn't on right
        rights = []
        for rule in rules:
            rights.append(rule[1])
        next_to_add = 0
        for rule in rules:
            if rule[0] not in rights:
                next_to_add = rule[0]
                break
        # ic(rights)
        ic(next_to_add)
        # add that number to master
        master.append(next_to_add)

        # remove rules that start with that number
        rules = [r for r in rules if r[0] != next_to_add]

        # call recursion
        return recursion(rules)
    return recursion(rules)



def main():
    rules, updates = gather_rules_and_updates()
    test_rules(rules)
    test_updates(updates)
    total = 0
    master_rule = assemble_master_rule(rules)
    ic(master_rule)
    # rejected_updates = get_rejected_updates(updates, rules)
    
    # fixed_updates = []
    # for u in rejected_updates:
    #     fixed = []
    #     for x in master_rule:
    #         if x in u:
    #             fixed.append(x)
    #     fixed_updates.append(fixed)
    # ic(fixed_updates)
    
    
    # for u in rejected_updates:
    #     ic(u, "before")
    #     repair_update(u, rules)
    #     if not verify_update(u, rules):
    #         ic(u, "after")
    # for update in rejected_updates:
    #     total += int(update[int((len(update)-1)/2)])
    
    
    
    ic(total)

if __name__ == "__main__":
    main()
