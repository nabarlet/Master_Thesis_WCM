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

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.range = [0.4, 0.6]

    __DEFAULT_ZONE_CONFIG__ = '2,3,4,5,1,1,1,1,1,1'
    @classmethod
    def create(cls, config_string = __DEFAULT_ZONE_CONFIG__):
        result = config_string.split(',')
        result = [int(n) for n in result]
        return cls(result)

    def generate(self):
        if not self.already_generated:
            d_indexes = list(exp_decile(len(self.composers), 10))
            d_indexes.append(len(self.composers)-1)
            comps = []
            cur = choice(self.composers[d_indexes[0]:d_indexes[1]])
            comps.append(cur)
            n = 1
            while (n < self.size):
                cur = self.next(comps, cur)
                comps.append(cur)
            shuffle(comps)
            self.generated = comps
        self.already_generated = True

    def next(self, already_found, seed):
        result = None
        pn = self.lookup(seed)
        results = pn.lookup_cross_range(self.range)
        if len(results) > 0:
            while True:
                result = choice(results) 
                if not result in already_found:
                    break
        else:
            #
            # DECIDE WHAT TO DO HERE (for example go back to already found)
            #
            pass
        return result

    def lookup(self, seed):
        result = None
        for pn in self.composers:
            if pn.nid == seed.nid:
                result = pn
                break
        return result

if __name__ == '__main__':
    config = PathPlaylist.__DEFAULT_ZONE_CONFIG__
    if len(sys.argv) > 1:
        config = sys.argv[1]
    zp = PathPlaylist.create(config)
    zp.print()
