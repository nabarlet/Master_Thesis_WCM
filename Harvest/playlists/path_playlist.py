import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from playlist import Playlist
from common.utilities.wcm_math import exp_decile
from utilities.plugs import exclusive_random

class PathPlaylist(Playlist):

    def __init__(self, rng):
        super().__init__()
        self.range = rng

    @classmethod
    def create(cls, rng):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        return cls(range)

    def generate(self):
        if not self.already_generated:
            comps = []
            n = 0
            cur = choice(self.zones[0])
            cur.zone = n
            comps.append(cur)
            while (n < self.size):
                n += 1
                possibilities = cur.lookup_cross_range(self.range)
                cur = self.next(comps, cur, possibilities)
                cur.zone = self.zone_lookup(cur)
                comps.append(cur)
            # shuffle(comps)
            self.generated = comps
        self.already_generated = True
        
    __WIDEN__= 0.1
    def next(self, already_found, seed, possibilities):
        result = None
        attempts = 0
        if len(possibilities) > 0:
            while attempts < 10:
                cross = choice(possibilities) 
                pn = cross.node
                pn.distance = cross.how_many_times
                if not pn in already_found:
                    result = pn
                    break
                attempts += 1
        if not result:
            idx = -2
            if len(already_found) < 3:
                idx = 0
            prev = already_found[idx]
            new_rng = [self.range[0] - PathPlaylist.__WIDEN__, self.range[1]]
            if new_rng[0]<0.0:
            	new_rng[0]=0.0
            	new_rng[1] += PathPlaylist.__WIDEN__
            	
            new_possibilities = prev.lookup_cross_range(new_rng)
            print("---> cannot find anything for %s, trying new_possibilities for %s" % (seed.nid, prev.nid), file=sys.stderr)
            result = self.next(already_found, prev, new_possibilities)
        return result

if __name__ == '__main__':
    range = '0.0-0.3'
    if len(sys.argv) == 2:
        range  = sys.argv[1]
    zp = PathPlaylist.create(range)
    zp.print_csv("%s" %(range))
