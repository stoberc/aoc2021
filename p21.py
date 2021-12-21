import pdb

PUZZLE = [7, 8] # [4, 8]

locations = PUZZLE[:]
scores = [0, 0]
nextroll = 100 # not one because it advances before returning
nrolls = 0
currentplayer = 0 # instead of player 1, player 2, we'll use player0, player1 for indexing convenience

def getnextroll():
    global nextroll
    global nrolls
    nrolls += 1
    nextroll += 1
    if nextroll == 101:
        nextroll = 1
    return nextroll

def playturn():
    global currentplayer
    rolls = [getnextroll() for _ in range(3)]
    locations[currentplayer] = (locations[currentplayer] + sum(rolls) - 1) % 10 + 1
    scores[currentplayer] += locations[currentplayer]
    currentplayer = 1 - currentplayer
    
while max(scores) < 1000:
    playturn()

print("Part 1:", min(scores) * nrolls)

# Part 2: recursion w/ memoization
memo = {}
def numberofwins(score0, score1, location0, location1, currentplayer):
    if (score0, score1, location0, location1, currentplayer) in memo:
        return memo[(score0, score1, location0, location1, currentplayer)]
    location0bk = location0
    location1bk = location1
    score0bk = score0
    score1bk = score1
    wins0 = 0
    wins1 = 0
    for r1 in [1, 2, 3]:
        for r2 in [1, 2, 3]:
            for r3 in [1, 2, 3]:
                location0, location1, score0, score1 = location0bk, location1bk, score0bk, score1bk
                if currentplayer == 0:
                    location0 = (location0 + r1 + r2 + r3 - 1) % 10 + 1
                    score0 += location0
                    if score0 >= 21:
                        wins0 += 1
                    else:
                        a, b = numberofwins(score0, score1, location0, location1, 1)
                        wins0 += a
                        wins1 += b
                else:
                    location1 = (location1 + r1 + r2 + r3 - 1) % 10 + 1
                    score1 += location1
                    if score1 >= 21:
                        wins1 += 1
                    else:
                        a, b = numberofwins(score0, score1, location0, location1, 0)
                        wins0 += a
                        wins1 += b     
    location0, location1, score0, score1 = location0bk, location1bk, score0bk, score1bk
    memo[(score0, score1, location0, location1, currentplayer)] = (wins0, wins1)
    return (wins0, wins1)
        
print("Part 2:", max(numberofwins(0, 0, PUZZLE[0], PUZZLE[1], 0)))  

pdb.set_trace()
    