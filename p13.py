import pdb

FNAME = "in13.txt"

data = open(FNAME).read().split('\n\n')
coords = set([(int(i) for i in line.split(',')) for line in data[0].splitlines()])
folds = []
for line in data[1].splitlines():
    a, b = line.split()[-1].split('=')
    folds.append((a, int(b)))
    
def process_fold(coords, fold):
    outcoords = []
    symbol, val = fold
    for x, y in coords:
        if symbol == 'x':
            if x > val:
                x = val - (x - val)
        else:
            assert symbol == 'y'
            if y > val:
                y = val - (y - val)
        outcoords.append((x, y))
    return set(outcoords)

# process just the first fold for part 1
coords = process_fold(coords, folds[0])
print("Part 1:", len(coords))

# now process the rest of the folds
for fold in folds[1:]:
    coords = process_fold(coords, fold)
    
# now display the resultant points
WIDTH = max(x for x, y in coords)
HEIGHT = max(y for x, y in coords)

print("Part 2:")
for y in range(HEIGHT + 1):
    for x in range(WIDTH + 1):
        if (x, y) in coords:
            print('#', end = '')
        else:
            print('.', end = '')
    print()
#pdb.set_trace()
    