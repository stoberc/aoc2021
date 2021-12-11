import pdb

FNAME = "in11.txt"

def parse_line(line):
    return [int(i) for i in line.strip()]
    
map = [parse_line(line) for line in open(FNAME).readlines()]

WIDTH = len(map[0])
HEIGHT = len(map)

flash_count = 0 # total number of flashes over all iterations
all_flashed = False # has there been a case where every cell flashed yet?

def step():
    global flash_count
    global all_flashed
    all_flash_count = 0 # count number of flashes in just this iteration
    for x in range(WIDTH):
        for y in range(HEIGHT):
            map[y][x] += 1
    while any(any(i > 9 for i in line) for line in map):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if map[y][x] > 9:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and map[ny][nx] > 0:
                            map[ny][nx] += 1
                    map[y][x] = 0
                    flash_count += 1
                    all_flash_count += 1
    if all_flash_count == WIDTH * HEIGHT:
        print("Part 2:", iteration_count)
        all_flashed = True

iteration_count = 0
while iteration_count < 100 or not all_flashed:
    iteration_count += 1
    step()
    if iteration_count == 100:
        print("Part 1:", flash_count)

#pdb.set_trace()
