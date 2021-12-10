import pdb
import math

FNAME = "in9.txt"

def parse_line(line):
    return [int(i) for i in line.strip()]
    
data = [parse_line(i) for i in open(FNAME).readlines()]

width = len(data[0])
height = len(data)

risk = 0
# will fill this out with basinIDs growing outwards from known basins
# -2 signifies not yet explored
# -1 signifies not part of any basin (height 9)
# 0 ... n signifies the basinID of that location
basinmap = [[-2] * width for _ in range(height)] 
basinID = 0 # next available basinID for newly discovered low points
for x in range(width):
    for y in range(height):
        neighbors = []
        val = data[y][x]
        if val == 9:
            basinmap[y][x] = -1
            continue            
        if x > 0:
            neighbors.append(data[y][x - 1])
        if x < width - 1:
            neighbors.append(data[y][x + 1])
        if y > 0:
            neighbors.append(data[y - 1][x])
        if y < height - 1:
            neighbors.append(data[y + 1][x])
        # low points contribute to risk and are assigned a fresh basinID
        if all([val < n for n in neighbors]):
            risk += val + 1
            basinmap[y][x] = basinID
            basinID += 1
print("Part 1:", risk)

# now we iterate through the map growing basins until no unknowns remain
# I suspect we could do this a little more efficiently, e.g. marking a location
# done so we don't keep checking it over and over, but this works and only takes
# something like ten iterations, which is aok
while -2 in [min(line) for line in basinmap]:
    for x in range(width):
        for y in range(height):
            if basinmap[y][x] > -1:
                if x > 0 and data[y][x] < data[y][x - 1] < 9:
                    basinmap[y][x - 1] = basinmap[y][x]
                if x < width - 1 and data[y][x] < data[y][x + 1] < 9:
                    basinmap[y][x + 1] = basinmap[y][x]
                if y > 0 and data[y][x] < data[y - 1][x] < 9:
                    basinmap[y - 1][x] = basinmap[y][x]
                if y < height - 1 and data[y][x] < data[y + 1][x] < 9:
                    basinmap[y + 1][x] = basinmap[y][x]

# find the size of each basin and multiply the top three
basinSizes = [sum(line.count(i) for line in basinmap) for i in range(0, basinID)]
basinSizes.sort()
print("Part 2:", math.prod(basinSizes[-3:]))

#pdb.set_trace()
    