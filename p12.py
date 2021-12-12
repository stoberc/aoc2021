import pdb

FNAME = "in12.txt"

edges = [line.split('-') for line in open(FNAME).read().splitlines()]

# find the set of all vertices, then classify them as small or big
# start and end are treated distinctly from small caves since they
# are terminating
all_caves = []
for x, y in edges:
    all_caves.append(x)
    all_caves.append(y)
all_caves = set(all_caves)
big_caves = set(i for i in all_caves if i[0].isupper())
small_caves = all_caves - big_caves - set(['start', 'end'])

# set up the adjacency list representation of the graph
neighbors = {}
for i in all_caves:
    neighbors[i] = []
    for x, y in edges:
        if x == i:
            neighbors[i].append(y)
        elif y == i:
            neighbors[i].append(x)

# given a sequence so far, give all valid next steps
def all_next_steps(sequence):
    next_steps = []
    prev = sequence[-1]
    if prev == 'end':
        return []
    for n in neighbors[prev]:
        if n in small_caves and n not in sequence:
            next_steps.append(n)
        elif n in big_caves:
            next_steps.append(n)
        elif n == 'end':
            next_steps.append(n)
    return next_steps
    
def calculate_number_of_paths(part):
    partial_paths = [['start']]
    complete_paths = []
    while partial_paths:
        new_partial_paths = []
        for path in partial_paths:
            for n in all_next_steps(path):
                if n == 'end':
                    complete_paths.append(path + [n])
                else:
                    new_partial_paths.append(path + [n])
        partial_paths = new_partial_paths
    print(f"Part {part}: {len(complete_paths)}")

calculate_number_of_paths(1)

# redefine the function slightly differently, then repeat the exact same process
def all_next_steps(sequence):
    next_steps = []
    prev = sequence[-1]
    if prev == 'end':
        return []
    for n in neighbors[prev]:
        if n in small_caves and n not in sequence:
            next_steps.append(n)
        elif n in small_caves and max(sequence.count(i) for i in small_caves) < 2:
            next_steps.append(n)
        elif n in big_caves:
            next_steps.append(n)
        elif n == 'end':
            next_steps.append(n)
    return next_steps
    
calculate_number_of_paths(2)

#pdb.set_trace()
