import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, choices, shuffle
from db.db import DbPro
from movement_playlist import MovementPlaylist
from utilities.plugs import exclusive_random

class MovementPathPlaylist(MovementPlaylist):

    @classmethod
    def create(cls, mov, rng, cache = None):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        return cls(mov, range, cache)
        
    @classmethod
    def create_random_args(cls, cache = None):
        total = 0
        eras = [('Medieval', 29), ('Renaissance', 142),('Baroque', 468), ('Classical', 188), ('Romantic', 488), ('Modernism', 1288), ('Contemporary', 1441)]
        for e,v in eras:
            total +=v 
        weights = [v/float(total) for n,v in eras]
        era = choices(eras,weights = weights)
        ranges = [[0.0,0.1],[0.0,0.2],[0.1,0.2],[0.2,0.3],[0.0,0.3],[0.3,0.4],[0.4,0.5],[0.3,0.5],[0.5,0.7],[0.6,0.8],[0.8,1.0]]   
        rng = choice(ranges)
        return cls(era, rng, cache)

    def __init__(self, mov = 'Classical', rng = [0.0, 1.0], cache = None):
        super().__init__(mov, cache)
        self.range = rng
        self.mov_zones = [[] for z in range(len(self.zones))]
        for c in self.movement_composers:
            self.mov_zones[c.zone].append(c)
            
    def generate(self):
        comps = []
        if not self.already_generated:
            first_zone = self.lookup_first_zone()
            cur = choice(self.mov_zones[first_zone])
            cur = self.random_title(cur)
            comps.append(cur)
            for n in range(self.__size__-1):
                nxt = self.next(cur,comps)
                nxt = self.generate_title(cur, nxt)
                comps.append(nxt)
                cur = nxt
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
