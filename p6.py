import pdb

fname = "in6.txt"

class Fish():
    
    def __init__(self, lifespan, current):
        self.lifespan = lifespan
        self.current = current
        
    def age(self):
        self.current -= 1
        if self.current == -1:
            self.current = 6
            return Fish(8, 8)
        return None
        
    def __repr__(self):
        return str(self.current)
  
fishes = [Fish(6, int(i)) for i in open(fname).read().split(',')]

def genstep():
    global fishes
    nextgen = []
    for i in range(len(fishes)):
        baby = fishes[i].age()
        if baby:
            nextgen.append(baby)
    fishes += nextgen
    
for _ in range(80):
    genstep()
    
print(len(fishes))
pdb.set_trace()
    