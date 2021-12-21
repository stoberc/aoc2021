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
    locations = locationsbk = [location0, location1]
    scores = scoresbk = [score0, score1]
    wins = [0, 0]
    for r1 in [1, 2, 3]:
        for r2 in [1, 2, 3]:
            for r3 in [1, 2, 3]:
                locations = locationsbk[:]
                scores = scoresbk[:]
                locations[currentplayer] = (locations[currentplayer] + r1 + r2 + r3 - 1) % 10 + 1
                scores[currentplayer] += locations[currentplayer]
                if scores[currentplayer] >= 21:
                    wins[currentplayer] += 1
                else:
                    a, b = numberofwins(*scores, *locations, 1 - currentplayer)
                    wins[0] += a
                    wins[1] += b                  
    memo[(*scoresbk, *locationsbk, currentplayer)] = wins
    return wins
        
print("Part 2:", max(numberofwins(0, 0, *PUZZLE, 0)))  

#pdb.set_trace()
    