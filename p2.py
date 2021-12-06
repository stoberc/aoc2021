#import pdb

fname = "in2.txt"

def parse_line(line):
    a = line.split()
    a[1] = int(a[1])
    return a
    
data = [parse_line(i) for i in open(fname).readlines()]

x, y = 0, 0
for d, m in data:
    if d == 'forward':
        x += m
    elif d == 'up':
        y -= m
    elif d == 'down':
        y += m
    else:
        raise ValueError("Unrecognized")
print("Part 1: ", x * y)

x, y, aim = 0, 0, 0
for d, m in data:
    if d == 'forward':
        x += m
        y += aim * m
    elif d == 'up':
        aim -= m
    elif d == 'down':
        aim += m
    else:
        raise ValueError("Unrecognized")
print("Part 2: ", x * y)

#pdb.set_trace()
    