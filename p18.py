#import pdb
import copy

FNAME = "in18.txt"

data = [eval(line) for line in open(FNAME).read().splitlines()]

class SnailfishNumber:
    
    def __init__(self, values):
        assert len(values) == 2
        self.left = values[0]
        self.right = values[1]
        if not isinstance(self.left, int): # regular number or snailfish number?
            self.left = SnailfishNumber(self.left)
        if not isinstance(self.right, int): # regular number or snailfish number?
            self.right = SnailfishNumber(self.right)
        
    def reduce(self):
        while self.explode() or self.split():
            pass
    
    def explode(self, depth = 0):
        # max recursion depth, theoretically
        # return both values; responsibility falls on parent to eliminate this pair and replace w/ zero
        if depth == 4:
            assert isinstance(self.left, int) and isinstance(self.right, int)
            return self.left, 'left', self.right, 'right'
            
        # try exploding the left branch first
        if isinstance(self.left, SnailfishNumber):
            x = self.left.explode(depth + 1)
            # if we hear back that the explosion was possible and is finished, report up the chain
            if x == True: 
                return True
            # or if we get back two numbers, push them left and right and assign zero in place
            # only possible when you explode a pair of regular numbers at maxdepth = 4
            elif isinstance(x, tuple) and len(x) == 4:
                assert depth == 3
                assert x[1] == 'left' and x[3] == 'right'
                self.left = 0
                if isinstance(self.right, int):
                    self.right += x[2]
                else:
                    self.right.rightpush(x[2])
                return x[0], 'left'
            # or if we get back one number...
            elif isinstance(x, tuple) and len(x) == 2:
                # if it's to be pushed right, we just do it and report success
                if x[1] == 'right':
                    if isinstance(self.right, int):
                        self.right += x[0]
                    else:
                        self.right.rightpush(x[0])
                    return True
                # otherwise it needs to be pushed left, and we must pass it up the chain
                # otherwise it needs to be pushed left, and we must pass it up the chain
                assert x[1] == 'left'
                # if we're at the top level, the number just goes in the garbage and we report success
                if depth == 0:
                    return True
                # otherwise, pass it up the chain
                else:
                    return x
            else:
                assert x == False
                
        # if that didn't work, try exploding the right branch
        if isinstance(self.right, SnailfishNumber):
            x = self.right.explode(depth + 1)
            # if we hear back that the explosion was possible and is finished, report up the chain
            if x == True: 
                return True
            # or if we get back two numbers, push them left and right
            # only possible when you explode a pair of regular numbers at maxdepth = 4
            elif isinstance(x, tuple) and len(x) == 4:
                assert depth == 3
                assert x[1] == 'left' and x[3] == 'right'
                self.right = 0
                if isinstance(self.left, int):
                    self.left += x[0]
                else:
                    self.left.leftpush(x[0])
                return x[2], 'right'
            # or if we get back one number...
            elif isinstance(x, tuple) and len(x) == 2:
                # if it's to be pushed left, we just do it and report success
                if x[1] == 'left':
                    if isinstance(self.left, int):
                        self.left += x[0]
                    else:
                        self.left.leftpush(x[0])
                    return True
                # otherwise it needs to be pushed right, and we must pass it up the chain
                assert x[1] == 'right'
                # if we're at the top level, the number just goes in the garbage and we report success
                if depth == 0:
                    return True
                # otherwise, pass it up the chain
                else:
                    return x
            else:
                assert x == False
            
        # I guess neither branch was explodable
        return False
                
    # absorb a value that's being pushed right
    # i.e. add the value to the leftmost value in the serialized representation
    def rightpush(self, value):
        if isinstance(self.left, int):
            self.left += value
        else:
            self.left.rightpush(value)
            
    # absorb a value that's being pushed left
    # i.e. add the value to the rightmost value in the serialized representation
    def leftpush(self, value):
        if isinstance(self.right, int):
            self.right += value
        else:
            self.right.leftpush(value)        
           
    def split(self):
        if isinstance(self.left, int) and self.left >= 10:
            self.left = SnailfishNumber([self.left // 2, (self.left + 1) // 2])
            return True
        elif isinstance(self.left, SnailfishNumber) and self.left.split():
            return True
        elif isinstance(self.right, int) and self.right >= 10:
            self.right = SnailfishNumber([self.right // 2, (self.right + 1) // 2])
            return True
        elif isinstance(self.right, SnailfishNumber) and self.right.split():
            return True
        return False
            
    def magnitude(self):
        if isinstance(self.left, int):
            val1 = self.left
        else:
            val1 = self.left.magnitude()
        if isinstance(self.right, int):
            val2 = self.right
        else:
            val2 = self.right.magnitude()
        return 3 * val1 + 2 * val2  
        
    def __add__(self, other):
        x = SnailfishNumber([0, 0])
        x.left = copy.deepcopy(self)
        x.right = copy.deepcopy(other)
        x.reduce()
        return x
            
    def __repr__(self):
        return f'[{self.left},{self.right}]'
        
vals = [SnailfishNumber(i) for i in data]
accumulator = vals[0]
for sn in vals[1:]:
    accumulator += sn
print("Part 1:", accumulator.magnitude())

mags = []
for i in range(len(vals)):
    for j in range(1, len(vals)):
        mags.append((vals[i] + vals[j]).magnitude())
print("Part 2:", max(mags))

#pdb.set_trace()
    