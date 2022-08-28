import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from path_playlist import PathPlaylist, CandidateNotFound
from zone_playlist import ZonePlaylist
from common.utilities.wcm_math import decile, exp_decile
from common.utilities.string import __UNK__
from utilities.plugs import exclusive_random

class ZonePathPlaylist(ZonePlaylist):

    def __init__(self, config, rng, cache = None):
        super().__init__(config, cache)
        self.range = rng
        
    @classmethod
    def create_random_args(cls, cache = None):
        config = ZonePlaylist.__DEFAULT_ZONE_CONFIG__
        ranges = [[0.0,0.1],[0.0,0.2],[0.1,0.2],[0.2,0.3],[0.0,0.3],[0.3,0.4],[0.4,0.5],[0.3,0.5],[0.5,0.7],[0.6,0.8],[0.8,1.0]]   
        rng = choice(ranges)
        return cls(config, rng, cache)

    @classmethod
    def create(cls, rng, config_string = ZonePlaylist.__DEFAULT_ZONE_CONFIG__, cache = None):
        rngs = rng.split('-')
        range = [float(r) for r in rngs]
        conf = config_string.split(',')
        conf = [int(n) for n in conf]
        return cls(conf, range, cache)

    def generate(self):
        if not self.already_generated:
            comps = []
            n = 0
            cur = choice(self.zones[0])
            cur.zone = n
            cur.title = super().generate_title(cur)
            comps.append(cur)
            n += 1
            while (n < len(self.zones)):                
                possibilities = cur.lookup_cross_range_and_zone(self.range, self.zones[n])
                n += 1
                try:
                    nxt = self.next(comps, cur, possibilities, n)
                    nxt.zone = self.zone_lookup(nxt)
                    nxt.title = self.generate_title(cur, nxt)
                    comps.append(nxt)
                    cur = nxt
                except CandidateNotFound:
                    break
            # shuffle(comps)
            self.generated = comps
        self.already_generated = True

    def generate_title(self, prev, nxt):
        result = __UNK__
        query = "SELECT R.title FROM record AS R JOIN record_performance AS RP, composer AS C, performance AS P \
                        WHERE RP.performance_id = P.id AND RP.record_id = R.id AND R.composer_id = C.id AND C.nid = ? \
                        AND P.id in (SELECT P2.id FROM record AS R2 JOIN record_performance AS RP2, composer AS C2, performance AS P2 \
                        WHERE RP2.performance_id = P2.id AND RP2.record_id = R2.id AND R2.composer_id = C2.id AND C2.nid = ?);"
        values = (nxt.nid, prev.nid,)
        results = self.db.query(query, values)
        if results and len(results) > 0:
            result = choice(results)[0]

        return result

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
        
    def print_csv(self, args = '', file = sys.stdout):
        super().print_csv(args=str(self.range), file = file)

if __name__ == '__main__':
    config = ZonePathPlaylist.__DEFAULT_ZONE_CONFIG__
    rng_string = '0.0-0.3'
    if len(sys.argv) > 1:
        config = sys.argv[1]
    if len(sys.argv) > 2:
        rng_string = sys.argv[2]
    zpp = ZonePathPlaylist.create(rng_string, config)
    zpp.print_csv(config)
