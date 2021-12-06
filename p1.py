import pdb

fname = "in1.txt"

#import maputil
#map = maputil.load(fname)

def parse_line(line):
    return int(line)
    
data = [parse_line(i) for i in open(fname).readlines()]

count1 = 0
for i in range(1, len(data)):
    if data[i] > data[i - 1]:
        count1 += 1
print("Part 1:", count1)

sliding = []
for i in range(len(data) - 2):
    sliding.append(sum(data[i:i+3]))

count2 = 0
for i in range(1, len(sliding)):
    if sliding[i] > sliding[i - 1]:
        count2 += 1
print("Part 2:", count2)

#pdb.set_trace()
    