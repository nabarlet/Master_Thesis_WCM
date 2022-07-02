import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from movement_playlist import MovementPlaylist
from utilities.plugs import exclusive_random

class MovementPathPlaylist(MovementPlaylist):

    @classmethod
    def create(cls, mov, rng):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        return cls(mov,range)

    def __init__(self, mov = 'Classical', rng = [0.0, 1.0]):
        super().__init__(mov)
        self.range = rng
        self.mov_zones = [[] for z in range(len(self.zones))]
        for c in self.movement_composers:
            self.mov_zones[c.zone].append(c)
            
    def generate(self):
        comps = []
        if not self.already_generated:
            first_zone = self.lookup_first_zone()
            cur = choice(self.mov_zones[first_zone])
            comps.append(cur)
            for n in range(self.size-1):
                pn = self.next(cur,comps)
                comps.append(pn)
            #shuffle(comps)
            self.generated = comps
        self.already_generated = True
        
    def lookup_first_zone(self):
        result=100
        for idx,pn in enumerate(self.movement_composers):
            if pn.zone < result:
                result=pn.zone
        return result
        
    def next(self, cur, already_found):
        result = None
        possibilities = []
        temp = cur.lookup_cross_range(self.range)
        for c in temp:
            if c.node.name == cur.name:
        	    continue
            if c.node.movement_name ==self.movement:
                (c.node.log_distance, c.node.lin_distance) = (c.log_distance, c.lin_distance)
                possibilities.append(c.node)
        if len(possibilities) < 1:
            print("%s does not cross with his own movement" %(cur.name), file = sys.stderr)
        
        result = exclusive_random(possibilities,already_found)
        return result   
                

if __name__ == '__main__':
    mov = 'Classical'
    rng = "0.0-1.0"
    if len(sys.argv) > 2:
        mov = sys.argv[1]
        rng = sys.argv[2]
    mp = MovementPathPlaylist.create(mov, rng)
    mp.print_csv("%s %s" %(mov,rng))
    
    mp.print_stats()
