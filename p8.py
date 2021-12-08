import pdb
from itertools import permutations

FNAME = "in8.txt"

# translation between segments and values
DIGIT_LUT = {'abcefg':0, 'cf':1, 'acdeg':2, 'acdfg':3, 'bcdf':4, 'abdfg':5, 'abdefg':6, 'acf':7, 'abcdefg':8, 'abcdfg':9}
    
def parse_line(line):
    return [tuple(sorted(i)) for i in line.replace('|','').split()]
data = [parse_line(i) for i in open(FNAME).readlines()]

# Part 1 asks us to count how many of the right-hand-side input strings
# have a length that makes them uniquely identifiable
count = 0
for line in data:
    for i in line[10:]:
        if len(i) in [2, 4, 3, 7]:
            count += 1
print("Part 1:", count)

# substitution cipher
def decrypt(msg, key):
    lut = {}
    for m, c in zip(key, 'abcdefg'):
        lut[m] = c
    return [lut[m] for m in msg]

# for each line, we find a mapping by brute force -
# 7! = 5040 permuations is tractable, though slow
# could certainly do something quite a bit more clever and faster
# like deduction based on the unique mappings, but that's a lot of work! ;)
outvals = [] # valid translations of each line's right hand side (rhs)
for i, line in enumerate(data):
    
    print(f"Processing line {i}/{len(data)}...")
    
    rhs = line[10:] # will only be translated once - no backup needed
        
    for key in permutations('abcdefg'):
        lhs = line[:10] # translate once per key
        lhs = tuple([''.join(sorted(decrypt(i, key))) for i in lhs]) # try the key
        if set(lhs) == set(DIGIT_LUT.keys()): # see if the key yielded the correct set of outputs
            # decrypt the right hand side using this key
            rhs = tuple([''.join(sorted(decrypt(i, key))) for i in rhs])
            out = '' # why do math when we have string manipulation?! ;)
            for i in rhs:
                out += str(DIGIT_LUT[i])
            outvals.append(int(out))
            break
        
print("Part 2:", sum(outvals))
    
#pdb.set_trace()

    