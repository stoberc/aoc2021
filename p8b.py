# an enhanced alternative approach for Day 8
import pdb

FNAME = "in8.txt"

def parse_line(line):
    return [set(i) for i in line.replace('|','').split()]
data = [parse_line(i) for i in open(FNAME).readlines()]

# Part 1 asks us to count how many of the right-hand-side input strings
# have a length that makes them uniquely identifiable
count = 0
for line in data:
    for i in line[10:]:
        if len(i) in [2, 4, 3, 7]:
            count += 1
print("Part 1:", count)

# digest a line - determine the numeral assignments based on lhs,
# then return value on rhs
def process(line):
    lhs = line[:10] # left hand side of pipe
    rhs = line[10:] # right hand side 
    assignments = [None] * 10 # assignments from digits to segment sets
    
    # sequential rules for assigning sets to numerals
    rules = []
    # an entry with just two segments must be the one; similar rules for 7, 4, 8
    rules.append((lambda i: len(i) == 2, 1))
    rules.append((lambda i: len(i) == 3, 7))
    rules.append((lambda i: len(i) == 4, 4))
    rules.append((lambda i: len(i) == 7, 8))
    # a five-segment character containing one must be three
    rules.append((lambda i: len(i) == 5 and all([j in i for j in assignments[1]]), 3))
    # a remaining five-segment character overlapping three semgents with 
    # four must be five
    rules.append((lambda i: len(i) == 5 and len(i.intersection(assignments[4])) == 3, 5))     
    # the last remaining five-segment character must be two
    rules.append((lambda i: len(i) == 5, 2))     
    # the (six-segment) character containing four must be nine
    rules.append((lambda i: all([j in i for j in assignments[4]]), 9))     
    # the remaining (six-segment) character containing one must be zero
    rules.append((lambda i: all([j in i for j in assignments[1]]), 0))     
    # the last remaining (six-segment) character must be six
    rules.append((lambda i: True, 6))

    for rule, value in rules:
        for i in lhs:
            if rule(i):
                assignments[value] = i
                lhs.remove(i)
                break

    # now translate the rhs and return
    return int(''.join([str(assignments.index(i)) for i in rhs]))

    
outvals = [process(line) for line in data]
print("Part 2:", sum(outvals))
    
#pdb.set_trace()

    