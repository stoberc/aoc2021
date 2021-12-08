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
    
    # an entry with just two segments must be the one
    for i in lhs:
        if len(i) == 2:
            assignments[1] = i
            lhs.remove(i)
            break
    
    # an entry with exactly three segments must be the seven
    for i in lhs:
        if len(i) == 3:
            assignments[7] = i
            lhs.remove(i)
            break
    
    # an entry with exactly four segments must be the four
    for i in lhs:
        if len(i) == 4:
            assignments[4] = i
            lhs.remove(i)
            break
    
    # an entry with all seven segments must be the eight
    for i in lhs:
        if len(i) == 7:
            assignments[8] = i
            lhs.remove(i)
            break
    
    # a five-segment character containing one must be three
    for i in lhs:
        if len(i) == 5 and all([j in i for j in assignments[1]]):
            assignments[3] = i
            lhs.remove(i)
            break
        
    # a remaining five-segment character overlapping three semgents with 
    # four must be five
    for i in lhs:
        if len(i) == 5 and len(i.intersection(assignments[4])) == 3:
            assignments[5] = i
            lhs.remove(i)
            break
      
    # the last remaining five-segment character must be two
    for i in lhs:
        if len(i) == 5:
            assignments[2] = i
            lhs.remove(i)
            break
     
    # the (six-segment) character containing four must be nine
    for i in lhs:
        if all([j in i for j in assignments[4]]):
            assignments[9] = i
            lhs.remove(i)
            break

    # the remaining (six-segment) character containing one must be zero
    for i in lhs:
        if all([j in i for j in assignments[1]]):
            assignments[0] = i
            lhs.remove(i)
            break
    
    # the last remaining (six-segment) character must be six
    assignments[6] = lhs[0]
    
    # now translate the rhs and return
    return int(''.join([str(assignments.index(i)) for i in rhs]))

    
outvals = [process(line) for line in data]
print("Part 2:", sum(outvals))
    
#pdb.set_trace()

    