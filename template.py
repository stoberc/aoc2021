import pdb
from collections import defaultdict
from aoc_utils import *
import re

FNAME = "in19.txt"

#import maputil
#map = maputil.load(FNAME)

def parse_line(line):
    return int(line)
    #return [int(i) for i in re.findall('(-?\d+)', line)] # grab all the numbers

#chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
data = [parse_line(line) for line in open(FNAME).read().splitlines()] # in chunks[0]]
#data = [int(i) for i in open(FNAME).read().split(',')]


pdb.set_trace()
    