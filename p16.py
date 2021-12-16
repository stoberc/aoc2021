import pdb
import math

FNAME = "in16.txt"

sequence = open(FNAME).read().strip()
sequence = ''.join([bin(int(i, 16))[2:].zfill(4) for i in sequence])

class Packet:
    
    def __init__(self, sequence):
        self.version = int(sequence[:3], 2)
        self.typeID = int(sequence[3:6], 2)
        self.subpackets = []
        if self.typeID == 4:
            i = 6
            value = ''
            while sequence[i] == '1':
                value += sequence[i+1:i+5]
                i += 5
            assert sequence[i] == '0'
            value += sequence[i+1:i+5]
            i += 5
            self.value = int(value, 2) # literal value
            self.bitlength = i # total number of bits in this packet
            self.residual = sequence[i:] # bits left over - future packets
        else:
            self.lengthtypeID = sequence[6]
            if self.lengthtypeID == '0':
                self.payload_length = int(sequence[7:22], 2)
                self.bitlength = 22 + self.payload_length
                payloadbits = sequence[22:]
                bitsremaining = self.payload_length
                while bitsremaining > 0:
                    subpacket = Packet(payloadbits)
                    self.subpackets.append(subpacket)
                    payloadbits = subpacket.residual
                    bitsremaining -= subpacket.bitlength
                assert bitsremaining == 0
                self.residual = payloadbits
                    
            else:
                assert self.lengthtypeID == '1'
                self.nsubpackets= int(sequence[7:18], 2)
                self.bitlength = 18
                payloadbits = sequence[18:]
                for _ in range(self.nsubpackets):
                    subpacket = Packet(payloadbits)
                    self.subpackets.append(subpacket)
                    self.bitlength += subpacket.bitlength
                    payloadbits = subpacket.residual
                self.residual = payloadbits
            if self.typeID == 0: # sum
                self.value = sum(sp.value for sp in self.subpackets)
            elif self.typeID == 1: # product
                self.value = math.prod(sp.value for sp in self.subpackets)
            elif self.typeID == 2: # min
                self.value = min(sp.value for sp in self.subpackets)
            elif self.typeID == 3: # max
                self.value = max(sp.value for sp in self.subpackets)
            elif self.typeID == 5: # greater than
                self.value = 1 if self.subpackets[0].value > self.subpackets[1].value else 0
            elif self.typeID == 6: # less than
                self.value = 1 if self.subpackets[0].value < self.subpackets[1].value else 0
            else:
                assert self.typeID == 7
                self.value = 1 if self.subpackets[0].value == self.subpackets[1].value else 0
                         
def versionsum(p):
    total = p.version
    for sp in p.subpackets:
        total += versionsum(sp)
    return total
        
p = Packet(sequence)
print("Part 1:", versionsum(p))
print("Part 2:", p.value)

pdb.set_trace()
    