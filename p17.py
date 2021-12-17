#import pdb
import re

FNAME = "in17.txt"

puzzle = open(FNAME).read().strip()
targetxmin, targetxmax, targetymin, targetymax = [int(i) for i in re.findall('(-?\d+)', puzzle)]

# because math...
# basically there exists some (several) x velocity such that it guarantees a high probe will hit x stasis
# w/in reasonable time well before the probe drops below zero. The probe is guaranteed to exactly pass down
# through zero at the initial y velocity, so we want the maximal y velocity that makes it just barely hit
# the the bottom of the target, i.e. vy = abs(targetymin) - 1. Using such a velocity, the max height achieved
# will be vy(vy + 1) // 2
print("Part 1:", targetymin * (targetymin + 1) // 2) 

# assuming all problem inputs meet these criteria
assert 0 < targetxmin < targetxmax
assert 0 > targetymax > targetymin

class Probe():
    
    def __init__(self, vx, vy):
        self.x, self.y = 0, 0
        self.vx, self.vy = vx, vy
        assert vx > 0 # no reason to shoot backwards
        self.maxx = self.vx * (self.vx + 1) // 2
        if self.vy > 0:
            self.maxy = self.vy * (self.vy + 1) // 2
        else:
            self.maxy = 0
    
    def step(self):
        self.x += self.vx
        self.y += self.vy
        if self.vx > 0:
            self.vx -= 1
        #elif self.vx < 0: # doesn't come up
        #    self.vx += 1
        self.vy -= 1

# we'll scan from the minimum vy = targetymin - 1 (otherwise you'll instatnly be beneath the target area)
# all the way up to the max vy = abs(targetymin), which would cause it to bypass entirely
# within each vy, we'll start w/ vx = 1 (could calculate more reasonable lower bound, but eh)
# and increase it until hitting the target becomes untenable (i.e. vx > targetxmax)
vy = targetymin - 1 # any smaller y velocity and you'll immediately be beneath the target area
count = 0 # for Part 2 - how many initial conditions lead to a hit?
part1 = 0
for vy in range(targetymin, -targetymin):
    for vx in range(1, targetxmax + 1):
        p = Probe(vx, vy)
        if p.maxx < targetxmin: # if we can't ever reach the targetxmin, don't bother
            continue
        while p.x < targetxmin: # step until we reach the targetxmin
            p.step()
        if p.y < targetymin: # if we've already missed in terms of y, move on
            continue
        # while hope remains to hit the target, advance and check again
        while p.x <= targetxmax and p.y >= targetymin:
            if targetxmin <= p.x <= targetxmax and targetymin <= p.y <= targetymax:
                count += 1
                #print(vx, vy, p.maxy, count)
                if p.maxy > part1:
                    part1 = p.maxy
                break
            p.step()
        
print("Part 1:", part1)
print("Part 2:", count)

#pdb.set_trace()
    