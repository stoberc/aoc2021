#import pdb
from collections import defaultdict

FNAME = "in15.txt"

risk_grid = [[int(i) for i in line] for line in open(FNAME).read().splitlines()]

# find the minimum risk from the top left corner of the grid to the bottom right corner
def calculate_min_risk(risk_grid):
    width = len(risk_grid[0])
    height = len(risk_grid)

    total_risk = {}
    total_risk[(width - 1, height - 1)] = 0

    potential_total_risk = defaultdict(lambda: float('inf'))
    potential_total_risk[(width - 1, height - 2)] = risk_grid[height - 1][width - 1]
    potential_total_risk[(width - 2, height - 1)] = risk_grid[height - 1][width - 1]

    while True:
        # our minimal candidate for potential total risk can be certified as such
        
        # find the minimal value + associated coordinates
        next_addition_risk = min(potential_total_risk.values())
        for k in potential_total_risk:
            if potential_total_risk[k] == next_addition_risk:
                break
                
        # check for goal
        x, y = k
        if (x, y) == (0, 0): # goal met
            return next_addition_risk
            
        # certify it and delete it from the queue
        total_risk[k] = next_addition_risk
        del potential_total_risk[k]
        
        # update neighbors
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            nx = x + dx
            ny = y + dy
            if (nx, ny) not in total_risk and 0 <= nx < width and 0 <= ny < height:
                potential_total_risk[(nx, ny)] = min(potential_total_risk[(nx, ny)], next_addition_risk + risk_grid[y][x])
                
print("Part 1:", calculate_min_risk(risk_grid))

# Part 2: create the expanded grid, then recalculate

# increase w/ wraparound from 9 to 1
def increment(x):
    if x == 9:
        return 1
    return x + 1

width = len(risk_grid[0])
height = len(risk_grid)

# flesh out the top rows of the risk grid to full width
for i in range(len(risk_grid)):
    for _ in range(width * 4):
        risk_grid[i].append(increment(risk_grid[i][-width]))
        
# extend to full column height
for _ in range(height * 4):
    row = []
    for i in range(width * 5):
        row.append(increment(risk_grid[-height][i]))
    risk_grid.append(row)

print("Part 2:", calculate_min_risk(risk_grid))

#pdb.set_trace()
    