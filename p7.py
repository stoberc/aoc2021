import pdb

FNAME = "in7.txt"
positions = [int(i) for i in open(FNAME).read().split(',')]

# reasonable bounds for optimal position
p0 = min(positions)
p1 = max(positions)

scores = [sum([abs(anchor - x) for x in positions]) for anchor in range(p0, p1 + 1)]
print("Part 1:", min(scores))

scores = [sum([abs(anchor - x) * (abs(anchor - x) + 1) // 2 for x in positions]) for anchor in range(p0, p1 + 1)]
print("Part 2:", min(scores))

#pdb.set_trace()
