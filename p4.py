import pdb

fname = "in4.txt"

class Board():
    
    def __init__(self, values):
        self.values = values
        self.called = [False for _ in values]
        self.most_recent = None
        
    def mark(self, value):
        for i in range(len(self.values)):
            if self.values[i] == value:
                self.called[i] = True
                self.most_recent = value
                #return # presumably repeats are impossible?
            
    def is_complete(self):
        rows = (all(board.called[i:i+5]) for i in range(0, 25, 5))
        cols = (all(board.called[i::5]) for i in range(5))
        return any(rows) or any(cols)
        
    def score(self):
        return sum([value for value, called in zip(self.values, self.called) if not called]) * self.most_recent

        
data = open(fname).read().split('\n\n')
calls = [int(i) for i in data[0].split(',')]
boards = [Board([int(i) for i in board.split()]) for board in data[1:]]

part1Done = False
for call in calls:
    removeq = []
    for board in boards:
        board.mark(call)
        if board.is_complete():
            if not part1Done:
                print("Part 1:", board.score())
                part1Done = True
            removeq.append(board)
    for board in removeq:
        boards.remove(board)
    if len(boards) == 1:
        break
       
board = boards[0]
for call in calls: # could track and start back where we left off, but just being lazy
    board.mark(call)
    if board.is_complete():
        print("Part 2:", board.score())
        break
    
pdb.set_trace()
    