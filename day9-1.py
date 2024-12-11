# day 9-1

from icecream import ic
from pathlib import Path
from collections import deque

input = Path("day9input.txt")
# input = Path("day9inputTEST.txt")

data = None
front_count = 0
back_count = 999

def get_data():
    with input.open() as f:
        data = f.readline()
    return data

def more_front():
    global front_count
    try:
        a = data.pop(0)
        assert int(a) != 0
    except IndexError:
        return ['.']
    try:
        b = data.pop(0)
        blah = [str(front_count),]*int(a)
        blah.extend('.'*int(b))
        return blah
    except IndexError:
        return [str(front_count),]*int(a)

def more_back():
    global back_count
    try:
        a = data.pop()
        assert int(a) != 0
    except IndexError:
        return []
    try:
        data.pop()
    except IndexError:
        pass
    return [str(back_count),]*int(a)

def main():
    global data
    global back_count
    global front_count

    data = list(get_data())

    # final file ID
    back_count = int((len(data)-1)/2)

    front = deque(more_front())
    back = deque(more_back())
    distance = 0
    checksum = 0

    while True:
        i = front.popleft()
        if i.isnumeric(): # testing for free space
            checksum += int(i) * distance # multiply by distance, add to total
        else:
            j = back.popleft() # grab off back
            checksum += int(j) * distance # multiply by distance, add to total

        # increment distance
        distance += 1

        # fill queues if they're empty
        if not back:
            back_count -= 1 # decrement file ID
            back.extend(more_back())
        if not front:
            front_count += 1 # increment file ID
            front.extend(more_front())

        # test to see if we're done
        # back empty, and front only free space
        if not back:
            # if front is just '.' we're done
            if [a for a in front if a == '.']:
                break
    ic(checksum)

if __name__ == "__main__":
    main()
