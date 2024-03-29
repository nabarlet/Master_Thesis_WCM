import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle, random
from db.db import DbPro
from playlist import Playlist
from common.utilities.wcm_math import exp_decile
from utilities.plugs import exclusive_random

class CandidateNotFound(Exception):
    pass

class PathPlaylist(Playlist):

    def __init__(self, rng, cache = None):
        super().__init__(cache)
        self.range = rng

    @classmethod
    def create(cls, rng, cache = None):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        return cls(range, cache)
        
    @classmethod
    def create_random_args(cls, cache = None):
        ranges = [[0.0,0.1],[0.0,0.2],[0.1,0.2],[0.2,0.3],[0.0,0.3],[0.3,0.4],[0.4,0.5],[0.3,0.5],[0.5,0.7],[0.6,0.8],[0.8,1.0]]   
        rng = choice(ranges)
        return cls(rng, cache)

    def generate(self):
        if not self.already_generated:
            comps = []
            n = 0
            cur = choice(self.zones[0])
            cur.zone = n
            cur.title = self.random_title(cur)
            comps.append(cur)
            while (n < self.__size__):
                n += 1
                possibilities = cur.lookup_cross_range(self.range)
                nxt = self.next(comps, cur, possibilities, 0)
                nxt.zone = self.zone_lookup(nxt)
                nxt.title = self.generate_title(cur, nxt)
                comps.append(nxt)
                cur = nxt
            # shuffle(comps)
            self.generated = comps
        self.already_generated = True
        
    __WIDEN__= 0.1
    def next(self, already_found, seed, possibilities, attempt):
        if attempt > 10:
            raise CandidateNotFound
        result = None
        attempts = 0
        if len(possibilities) > 0:
            while attempts < 10:
                cross = choice(possibilities) 
                pn = cross.node
                if not pn in already_found:
                    (pn.log_distance, pn.lin_distance) = (cross.log_distance, cross.lin_distance)
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
            result = self.next(already_found, prev, new_possibilities, attempt+1)
        return result

if __name__ == '__main__':
    range = '0.0-0.3'
    if len(sys.argv) == 2:
        range  = sys.argv[1]
    zp = PathPlaylist.create(range)
    zp.print_csv("%s" %(range))
