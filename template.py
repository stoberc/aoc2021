import pdb
from collections import defaultdict

fname = "in1.txt"

#import maputil
#map = maputil.load(fname)

def parse_line(line):
    return int(line)
    
data = [parse_line(i) for i in open(fname).readlines()]
#data = open(fname).read().split('\n\n')



pdb.set_trace()
    