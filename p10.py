import pdb

FNAME = "in10.txt"
data = open(FNAME).read().splitlines()

PENALTIES = {')':3, ']':57, '}':1197, '>':25137}
CLOSING_SCORES = {')':1, ']':2, '}':3, '>':4}

ENDINGS = {'(':')', '[':']', '{':'}', '<':'>'}
BEGINNINGS = {}
for k, v in ENDINGS.items():
    BEGINNINGS[v] = k
    
def corruption_score(line):
    stack = []
    for i in line:
        if i in BEGINNINGS.values():
            stack.append(i)
        elif stack[-1] != BEGINNINGS[i]:
            return PENALTIES[i]
        else:
            stack.pop(-1)
    return 0

scores = [corruption_score(line) for line in data]
print("Part 1:", sum(scores))

# filter out corrupt lines
data = [line for line in data if corruption_score(line) == 0]

def completion_score(line):
    stack = []
    for i in line:
        if i in BEGINNINGS.values():
            stack.append(i)
        else:
            stack.pop(-1)
    close_sequence = reversed([ENDINGS[i] for i in stack])
    score = 0
    for i in close_sequence:
        score *= 5
        score += CLOSING_SCORES[i]
    return score
    
scores = [completion_score(line) for line in data]
scores.sort()
print("Part 2:", scores[len(scores) // 2])

#pdb.set_trace()
    