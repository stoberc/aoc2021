import pdb

fname = "in6.txt"

countdowns = [int(i) for i in open(fname).read().split(',')]

# keep track of HOW MANY fish have x time until spawn instead of individual fish
fishcounts = [0] * 9
for countdown in countdowns:
    fishcounts[countdown] += 1
    
for i in range(256):
    # advance a generation
    spawn = fishcounts.pop(0) # all the fish at index 0 are ready to spawn
    fishcounts.append(spawn) # their babies go at the end (8)
    fishcounts[6] += spawn # they are reset to 6
    
    if i == 79:
        print("Part 1:", sum(fishcounts))     

print("Part 2:", sum(fishcounts))

#pdb.set_trace()
