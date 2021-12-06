import pdb
from collections import defaultdict

fname = "in5.txt"

def parse_line(line):
    return [int(i) for i in line.replace(' -> ', ',').split(',')]
    
points = [parse_line(i) for i in open(fname).readlines()]

covered = defaultdict(int)
for x0, y0, x1, y1 in points:
    if x0 == x1:
        for y in range(min(y0, y1), max(y0, y1) + 1):
            covered[(x0, y)] += 1
    elif y0 == y1:
        for x in range(min(x0, x1), max(x0, x1) + 1):
            covered[(x, y0)] += 1

print("Part 1:", sum(1 for v in covered.values() if v > 1))

covered = defaultdict(int)
for x0, y0, x1, y1 in points:
    if x0 == x1:
        for y in range(min(y0, y1), max(y0, y1) + 1):
            covered[(x0, y)] += 1
    elif y0 == y1:
        for x in range(min(x0, x1), max(x0, x1) + 1):
            covered[(x, y0)] += 1
    else:
        dx = 1 if x0 < x1 else -1
        dy = 1 if y0 < y1 else -1         
        for _ in range(abs(x0 - x1) + 1):
            covered[(x0, y0)] += 1
            x0 += dx
            y0 += dy
            
print("Part 2:", sum(1 for v in covered.values() if v > 1))

#pdb.set_trace()
    