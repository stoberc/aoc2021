import pdb
from collections import defaultdict

FNAME = "in1.txt"

#import maputil
#map = maputil.load(FNAME)

def parse_line(line):
    return int(line)
    
data = [parse_line(i) for i in open(FNAME).readlines()]
#data = [int(i) for i in open(FNAME).read().split(',')]
#data = open(FNAME).read().split('\n\n')



pdb.set_trace()
    