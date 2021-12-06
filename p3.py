import pdb

fname = "in3.txt"
    
data = open(fname).read().splitlines()

gamma = '0b'
epsilon = '0b'
for i in range(len(data[0])):
    col = [line[i] for line in data]
    if col.count('0') > col.count('1'):
        gamma += '0'
        epsilon += '1'
    else:
        gamma += '1'
        epsilon += '0'
print("Part 1:", eval(gamma) * eval(epsilon))
        
d = data[:]
i = 0
while len(d) > 1:
    col = [line[i] for line in d]
    if col.count('0') > col.count('1'):
        d = [j for j in d if j[i] == '0']
    else:
        d = [j for j in d if j[i] == '1']
    i += 1
oxy = eval('0b' + d[0])

d = data[:]
i = 0
while len(d) > 1:
    col = [line[i] for line in d]
    if col.count('0') <= col.count('1'):
        d = [j for j in d if j[i] == '0']
    else:
        d = [j for j in d if j[i] == '1']
    i += 1
co2 = eval('0b' + d[0])

print("Part 2:", oxy * co2)

#pdb.set_trace()
    