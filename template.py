import pdb
from collections import defaultdict

FNAME = "in14.txt"

#import maputil
#map = maputil.load(FNAME)

def parse_line(line):
    return int(line)
    
data = [parse_line(line) for line in open(FNAME).readlines()]
#data = [int(line) for line in open(FNAME).read().split(',')]
#data = open(FNAME).read().split('\n\n')



pdb.set_trace()
    