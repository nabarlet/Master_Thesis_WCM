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

class PathPlaylist(Playlist):

    def __init__(self, rng, config):
        super().__init__()
        self.config = config
        self.range = rng

    __DEFAULT_ZONE_CONFIG__ = '2,3,4,5,1,1,1,1,1,1'
    @classmethod
    def create(cls, rng, config_string = __DEFAULT_ZONE_CONFIG__):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        conf = config_string.split(',')
        conf = [int(n) for n in conf]
        return cls(range, conf)

    def generate(self):
        if not self.already_generated:
            d_indexes = list(exp_decile(len(self.composers), 20))
            d_indexes.append(len(self.composers)-1)
            comps = []
            n = 0
            cur = choice(self.composers[d_indexes[0]:d_indexes[1]])
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

    def next(self, already_found, seed, possibilities):
        result = None
        attempts = 0
        if len(possibilities) > 0:
            while attempts < 10:
                cross = choice(possibilities) 
                cross = cross.node
                if not cross in already_found:
                    result = cross
                    break
                attempts += 1
        if not result:
            idx = -2
            if len(already_found) < 3:
                idx = 0
            prev = already_found[idx]
            new_possibilities = prev.lookup_cross_range([0.0, 2.0])
            print("---> cannot find anything for %s, trying new_possibilities for %s" % (seed.nid, prev.nid), file=sys.stderr)
            result = self.next(already_found, prev, new_possibilities)
        return result

if __name__ == '__main__':
    config = PathPlaylist.__DEFAULT_ZONE_CONFIG__
    range = '0.0-0.3'
    if len(sys.argv) == 3:
        range  = sys.argv[1]
        config = sys.argv[2]
    if len(sys.argv) == 2:
        range  = sys.argv[1]
    zp = PathPlaylist.create(range, config)
    zp.print()
