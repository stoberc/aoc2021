import pdb
from itertools import permutations

FNAME = "in8.txt"

# translation back and forth between
DIGIT_LUT = {0:'abcefg', 1:'cf', 2:'acdeg', 3:'acdfg', 4:'bcdf', 5:'abdfg', 6:'abdefg', 7:'acf', 8:'abcdefg', 9:'abcdfg'}
REVERSE_DIGIT_LUT = {}
for k, v in DIGIT_LUT.items():
    REVERSE_DIGIT_LUT[v] = k
    
def parse_line(line):
    return [tuple(sorted(i)) for i in line.replace('|','').split()]
    
data = [parse_line(i) for i in open(FNAME).readlines()]
#data = [int(i) for i in open(FNAME).read().split(',')]
#data = open(FNAME).read().split('\n\n')

count = 0
for line in data:
    for code in line[10:]:
        if len(code) in [2, 4, 3, 7]:
            count += 1
print("Part 1:", count)

def translate(msg, key):
    lut = {}
    for m, c in zip(key, 'abcdefg'):
        lut[m] = c
    return [lut[m] for m in msg]

iaa = 0
outs = []
for line in data:
    
    lineDone = False
    
    lhsbk = line[:10]
    rhs = line[10:]
        
    for key in permutations('abcdefg'):
        #pdb.set_trace()
        lhs = lhsbk[:]
        lhs = tuple([''.join(sorted(translate(i, key))) for i in lhs])
        if set(lhs) == set(DIGIT_LUT.values()):
            print("HIT" + str(iaa))
            iaa += 1
            out = ''
            #pdb.set_trace()
            rhs = tuple([''.join(sorted(translate(i, key))) for i in rhs])
            #pdb.set_trace()
            for i in rhs:
                out += str(REVERSE_DIGIT_LUT[i])
            outs.append(int(out))
        
print("Part 2:", sum(outs))
    

pdb.set_trace()
    