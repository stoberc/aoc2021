import pdb
import copy

FNAME = "in19.txt"

scanner_chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]

class Scan:
    
    def __init__(self, scan_string):
        self.scanID = int(scan_string[0].split()[2])
        self.coords = tuple([tuple([int(i) for i in line.split(',')]) for line in scan_string[1:]])
        self.center = (0, 0, 0)

        # find the differential traces - the relative position from each beacon to all others
        self.traces = []
        for x, y, z in self.coords:
            row_trace = []
            for i, j, k in self.coords:
                row_trace.append((i - x, j - y, k - z))
            self.traces.append(row_trace)
        self.tracesets = [set(coordtrace) for coordtrace in self.traces]
        
        self.tracehashes = []
        for row in self.traces:
            for x, y, z in row:
                self.tracehashes.append(abs(x) + abs(y) + abs(z))
        self.tracehashes = set(self.tracehashes)
         
    def recenter(self, x, y, z):
        i, j, k = self.center
        dx, dy, dz = x - i, y - j, z - k
        if dx == dy == dz == 0:
            return
        self.center = (x, y, z)
        self.coords = tuple([(i + dx, j + dy, k + dz) for i, j, k in self.coords])
        
    def rotate_around_center(self, rotation):
        center_temp = self.center
        self.recenter(*[-i for i in center_temp])
        self.coords = [reassign_orientation(*coord, rotation) for coord in self.coords]
        self.recenter(*center_temp)
        self.traces = [[reassign_orientation(*coord, rotation) for coord in row] for row in self.traces]
        self.tracesets = [set(coordtrace) for coordtrace in self.traces]
        
    def is_probably_consistent(self, other, threshold = 12):
        return len(self.tracehashes.intersection(other.tracehashes)) >= threshold
        
    def is_consistent(self, other, threshold = 12):
        for i in self.tracesets:
            for j in other.tracesets:
                if len(i.intersection(j)) >= threshold: # TODO - check boundaries, overlap, etc.
                    return True
        return False
        
    def align(self, other, threshold = 12):
        for i in range(len(self.coords)):
            for j in range(len(other.coords)):
                if len(self.tracesets[i].intersection(other.tracesets[j])) >= threshold:
                    a, b, c = self.coords[i]
                    x, y, z = other.coords[j]
                    dx, dy, dz = a - x, b - y, c - z
                    x, y, z = other.center
                    other.recenter(x + dx, y + dy, z + dz)
                    #assert len(set(self.coords).intersection(set(other.coords))) >= threshold
                    # TODO - add checks that there's nothing spurious in the overlapping region
                    # I suspect the input is designed so that this is impossible, though.
                    # I.e. IF 12 beacons have a valid and consistent patial relationship,
                    # there won't be a 13th that is inconsistent in the overlapping region that
                    # invalidates the relationship.
                    return
        raise ValueError(f"scans {self.scanID} and {other.scanID} could not be aligned")
                    
    def manhattan_distance(self, other):
        a, b, c = self.center
        x, y, z = other.center
        return abs(a - x) + abs(b - y) + abs(c - z)
        
    def __repr__(self):
        return f"Scan: {self.scanID}\n{self.coords}\n"
                
# to find all possible rotation matrices,
# I *think* we want all 3x3 matrices with the following properties:
# 1 or -1 once in each row (zeros for the rest)
# ditto for columns
# determinant = 1 - I think otherwise you get a reflection too

def determinant(mat3x3):
    a, b, c = mat3x3[0]
    d, e, f = mat3x3[1]
    g, h, i = mat3x3[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    
# convert a 2d data structure into tuples
def tuplify2d(mat):
    return tuple([tuple(row) for row in mat])
    
rotation_matrices = []
for i in range(3):
    for j in range(3):
        if i == j:
            continue
        k =  3 - i - j
        for signx in [1, -1]:
            for signy in [1, -1]:
                for signz in [1, -1]:
                    matrix = [[0 for _ in range(3)] for _ in range(3)]
                    matrix[0][i] = signx
                    matrix[1][j] = signy
                    matrix[2][k] = signz
                    if determinant(matrix) == 1:
                        # make it immutable, just in case
                        matrix = tuplify2d(matrix)
                        rotation_matrices.append(matrix)
assert len(rotation_matrices) == 24

# naive but adequately efficient standard matrix multiplication
def matmult(a, b, immutable = True):
    n0 = len(a)
    m0 = len(a[0])
    n1 = len(b)
    m1 = len(b[0])
    assert m0 == n1
    matrix = []
    for row in range(n0):
        rowvals = []
        for col in range(m1):
            accumulator = 0
            for i in range(m0):
                accumulator += a[row][i] * b[i][col]
            rowvals.append(accumulator)
        matrix.append(rowvals)
    if immutable:
        matrix = tuplify2d(matrix)
    return matrix

# transform a set of coordinates according to a rotation matrix
def reassign_orientation(x, y, z, rotation, immutable = True):
    x, y, z = matmult(rotation, [[x], [y], [z]])
    result = x[0], y[0], z[0]
    if immutable:
        return tuple(result)
    return result
    
# Now that we have some of the fundamental building blocks in place, here's the idea:
# 1. Calculate how beacons are spatially related to each other for scanner 0 aka the differential trace.
#    I.e. the delta from every beacon to every other beacon. This differential trace should be identical
#    irrespective of which beacon is observing them, so long as you determine the appropriate rotation.
# 2. Try to find another scanner with a significantly overlapping differential trace. >= 12
#    This will require iterating through each scanner, calculating its trace, then iterating
#    through all 24 rotations to see if any are consistent.
#    If we find one, we can permanently apply this rotation to this scanner chunk so that it's orientation-
#    aligned with the zero basis.
#    We can then find the coordinates of this scanner relative to the basis scanner and permanently adjust
#    its readings to be in the absolute (scanner zero basis) reference frame.
# 3. At that point, we just repeat the process finding more and more scanners that overlap, until every single
#    scanner data set has been processed in this way.

scans = [Scan(chunk) for chunk in scanner_chunks]

aligned = [scans[0]] # we'll arbitrarily use the first scan as our reference frame
unaligned = scans[1:]

already_compared = {}
while unaligned:
    updated = False
    for unaligned_scan in unaligned: # TODO - more efficient to not reset back to start of unaligned after each new addition
        unaligned_scan_bk = copy.deepcopy(unaligned_scan)
        for aligned_scan in aligned:
            if (aligned_scan.scanID, unaligned_scan.scanID) in already_compared:
                continue
            already_compared[(aligned_scan.scanID, unaligned_scan.scanID)] = True
            already_compared[(unaligned_scan.scanID, aligned_scan.scanID)] = True
            if not aligned_scan.is_probably_consistent(unaligned_scan):
                continue
            for rotation in rotation_matrices:
                unaligned_scan = copy.deepcopy(unaligned_scan_bk)
                unaligned_scan.rotate_around_center(rotation)
                if aligned_scan.is_consistent(unaligned_scan):
                    aligned_scan.align(unaligned_scan)
                    aligned.append(unaligned_scan)
                    for i in range(len(unaligned)):
                        if unaligned[i].scanID == unaligned_scan.scanID:
                            del unaligned[i]
                            break
                    print("Aligned scan number", unaligned_scan.scanID, "to reference scan", aligned_scan.scanID)
                    updated = True
                    break
            if updated:
                break
        if updated:
            break
          
print("Part 1:", len(set(sum((list(scan.coords) for scan in aligned), []))))

mds = []
for i in range(len(aligned)):
    for j in range(i + 1, len(aligned)):
        mds.append(aligned[i].manhattan_distance(aligned[j]))
print("Part 2:", max(mds))
pdb.set_trace()
    
