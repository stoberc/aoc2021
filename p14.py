import pdb
from collections import defaultdict

FNAME = "in14.txt"

data = open(FNAME).read().split('\n\n')
pdb.set_trace()
base = data[0]
product = {}
for line in data[1].splitlines():
    a, b = line.split(" -> ")
    product[a] = b

# iterate the comopund forward one generation
# e.g. HH -> N means HH -> HNH
def step(compound):
    out = ''
    for i in range(len(compound) - 1):
        out += compound[i] + product[compound[i:i+2]]
    out += compound[-1]
    return out
    
# the original way for Part 1 - obsoleced but maintained for reference
#compound = base
#for _ in range(10):
#    compound = step(compound)
#
#counts = [(compound.count(i), i) for i in compound]
#counts.sort()
#print("Part 1:", counts[-1][0] - counts[0][0])

# return the count profile of a compound x steps from now
# will use recursion with memoization
memo = {}
def profile(compound, steps):
    
    if (compound, steps) in memo:
        return memo[(compound, steps)]
        
    # large compounds can just be broken into small compounds and recombined
    if len(compound) > 2:
        counts = defaultdict(int)
        for i in range(len(compound) - 1):
            subcounts = profile(compound[i:i+2], steps)
            for k, v in subcounts.items():
                counts[k] += v
        for c in compound[1:-1]: # correct for double counting the overlap
            counts[c] -= 1
        return counts       
        
    # other than at the top level, we can just deal with compounds of size 2
    assert len(compound) == 2
    
    # base cases
    if steps == 1:
        countdict = defaultdict(int)
        for c in step(compound):
            countdict[c] += 1
        memo[(compound, steps)] = countdict
        return countdict
        
    # for a new compound, iterate it forward a generation,
    # then find the counts of its children and recombine
    counts = defaultdict(int)
    nextgen = step(compound)
    left = nextgen[:2]
    right = nextgen[-2:]
    countsleft = profile(left, steps - 1)
    countsright = profile(right, steps - 1)
    for k, v in countsleft.items():
        counts[k] += v
    for k, v in countsright.items():
        counts[k] += v
    counts[nextgen[1]] -= 1 # correct for double counting the middle character
    memo[(compound, steps)] = counts # save it for later!
    return counts
    
counts = profile(base, 10)
print("Part 1:", max(counts.values()) - min(counts.values()))
counts = profile(base, 40)
print("Part 2:", max(counts.values()) - min(counts.values()))

#pdb.set_trace()
