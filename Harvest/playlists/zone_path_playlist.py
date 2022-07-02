import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from path_playlist import PathPlaylist
from zone_playlist import ZonePlaylist
from common.utilities.wcm_math import decile, exp_decile
from utilities.plugs import exclusive_random

class CandidateNotFound(Exception):
    pass

class ZonePathPlaylist(ZonePlaylist):

    def __init__(self, config, rng):
        super().__init__(config)
        self.range = rng

    @classmethod
    def create(cls, rng, config_string = ZonePlaylist.__DEFAULT_ZONE_CONFIG__):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        conf = config_string.split(',')
        conf = [int(n) for n in conf]
        return cls(conf, range)

    def generate(self):
        if not self.already_generated:
            comps = []
            n = 0
            cur = choice(self.zones[0])
            cur.zone = n
            comps.append(cur)
            while (n < len(self.zones)):
                n += 1
                possibilities = cur.lookup_cross_range_and_zone(self.range, self.zones[n])
                try:
                    cur = self.next(comps, cur, possibilities, n)
                    cur.zone = self.zone_lookup(cur)
                    comps.append(cur)
                except CandidateNotFound:
                    break
            # shuffle(comps)
            self.generated = comps
        self.already_generated = True

    def next(self, already_found, seed, possibilities, zone_number):
        result = None
        attempts = 0
        if len(possibilities) > 0:
            while attempts < 10:
                cross = choice(possibilities) 
                pn = cross.node
                (pn.log_distance, pn.lin_distance) = (cross.log_distance, cross.lin_distance)
                if not pn in already_found:
                    result = pn
                    break
                attempts += 1
        if not result:
            idx = -2
            if len(already_found) < 3:
                idx = 0
            prev = already_found[idx]
            new_rng = [self.range[0] - PathPlaylist.__WIDEN__, self.range[1] + PathPlaylist.__WIDEN__]
            if new_rng[0]<0.0:
            	new_rng[0]=0.0
            	
            zone_number += 1
            if zone_number >= len(self.zones):
                raise CandidateNotFound
            new_possibilities = prev.lookup_cross_range_and_zone(new_rng, self.zones[zone_number])
            print("---> cannot find anything for %s, trying new_possibilities for %s" % (seed.nid, prev.nid), file=sys.stderr)
            result = self.next(already_found, prev, new_possibilities, zone_number)
        return result

if __name__ == '__main__':
    config = ZonePathPlaylist.__DEFAULT_ZONE_CONFIG__
    rng_string = '0.0-0.3'
    if len(sys.argv) > 1:
        config = sys.argv[1]
    if len(sys.argv) > 2:
        rng_string = sys.argv[2]
    zpp = ZonePathPlaylist.create(rng_string, config)
    zpp.print_csv(config)
    
    print(zpp.stat_top_era(),file=sys.stderr)
