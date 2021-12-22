import pdb
import re

FNAME = "in22.txt"

def parse_line(line):
    return [line.split()[0]] + [int(i) for i in re.findall('(-?\d+)', line)] # grab command + all the numbers

commands = [parse_line(line) for line in open(FNAME).read().splitlines()]

# naive approach to Part 1: keep track of every individual cube
# could just solve alongside Part 2, but keeping original algo for posterity
oncubes = {}
for status, xmin, xmax, ymin, ymax, zmin, zmax in commands:
    if xmin < -50 or xmin > 50 or ymin < -50 or ymax > 50 or zmin < -50 or zmax > 50:
        continue
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                if status == 'on':
                    oncubes[(x, y, z)] = True
                elif (x, y, z) in oncubes:
                    del oncubes[(x, y, z)]
print("Part 1:", len(oncubes))

# for very large boxes, need to keep track of the box as a whole entity,
# not just a very large conglomerate of individual cubes
class Box:
    
    def __init__(self, status, xmin, xmax, ymin, ymax, zmin, zmax):
        self.status = status
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        
    # how many cubes are in this box?
    def get_number_of_cubes(self):
        return (self.xmax - self.xmin + 1) * (self.ymax - self.ymin + 1) * (self.zmax - self.zmin + 1)
        
    # does the other box overlap this one at all?
    # just one giant compound boolean
    def overlaps(self, other):
        return (other.xmax >= self.xmin and other.xmin <= self.xmax and 
            other.ymax >= self.ymin and other.ymin <= self.ymax and
            other.zmax >= self.zmin and other.zmin <= self.zmax)
       
    # returns the box representing the overlapping region between two boxes
    def intersection(self, other):
        if not self.overlaps(other):
            return None
        return Box('unknown', max(self.xmin, other.xmin), min(self.xmax, other.xmax),
                max(self.ymin, other.ymin), min(self.ymax, other.ymax),
                max(self.zmin, other.zmin), min(self.zmax, other.zmax))
        
    # subtract another box from this one
    # depending on how the regions overlap, this may return between one and six boxes
    # basically focusses on one dimension at a time:
    # 1. find any box that exists on the minimum x side, full in y and z
    # 2. ditto for maximum x side
    # 3. anything that still remains must align in x, so repeat for yminside, ymaxside
    # 4. anything that still remains must align in x, and y; repeat for z min/max
    def __sub__(self, other):
        assert self.overlaps(other)
        outboxes = []
        if self.xmin < other.xmin: # xminside
            outboxes.append(Box(self.status, self.xmin, other.xmin - 1, self.ymin, self.ymax, self.zmin, self.zmax))
        if self.xmax > other.xmax: # xmaxside
            outboxes.append(Box(self.status, other.xmax + 1, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax))
        if self.ymin < other.ymin: # yminside
            outboxes.append(Box(self.status, max(self.xmin, other.xmin), min(self.xmax, other.xmax), self.ymin, other.ymin - 1, self.zmin, self.zmax))
        if self.ymax > other.ymax: # ymaxside
            outboxes.append(Box(self.status, max(self.xmin, other.xmin), min(self.xmax, other.xmax), other.ymax + 1, self.ymax, self.zmin, self.zmax))
        if self.zmin < other.zmin: # zminside
            outboxes.append(Box(self.status, max(self.xmin, other.xmin), min(self.xmax, other.xmax), max(self.ymin, other.ymin), min(self.ymax, other.ymax), self.zmin, other.zmin - 1))
        if self.zmax > other.zmax: # zmaxside
            outboxes.append(Box(self.status, max(self.xmin, other.xmin), min(self.xmax, other.xmax), max(self.ymin, other.ymin), min(self.ymax, other.ymax), other.zmax + 1, self.zmax))
        return outboxes
    
    # returns a list of boxes representing all the space outside of other but inside of self 
    # important to leave other intact in case it overlaps other boxes too
    def cutout(self, other):
        assert self.status == 'on'
        if not self.overlaps(other):
            return [self]
        overlap = self.intersection(other)
        return self - overlap
        
    def __repr__(self):
        return f"Box({self.status}, {self.xmin}, {self.xmax}, {self.ymin}, {self.ymax}, {self.zmin}, {self.zmax})"
        
# now for each on command we add the box to on_boxes, possibly fracturing other on boxes as we go
# for each off command, we simply fracture any on boxes to retain what stays on
on_boxes = [] # invariant: these boxes don't overlap
for command in commands:
    b = Box(*command)
    on_boxes_next_generation = []
    if b.status == 'on':
        on_boxes_next_generation.append(b)
    for box in on_boxes:
        on_boxes_next_generation += box.cutout(b)
    on_boxes = on_boxes_next_generation
print("Part 2:", sum(b.get_number_of_cubes() for b in on_boxes))
        
#pdb.set_trace()
    