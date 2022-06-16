import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from playlist import Playlist
from common.utilities.wcm_math import decile

class ZonePlaylist(Playlist):

    def __init__(self, config):
        super().__init__()
        self.config = config

    __DEFAULT_ZONE_CONFIG__ = '2,3,4,5,1,1,1,1,1,1'
    @classmethod
    def create(cls, config_string = __DEFAULT_ZONE_CONFIG__):
        result = config_string.split(',')
        result = [int(n) for n in result]
        return cls(result)

    def generate(self):
        if not self.already_generated:
            d_indexes = decile(len(self.composers), 10)
            d_indexes.append(len(self.composers)-1)
            start = d_indexes[0]
            comps = []
            for idx, end in enumerate(d_indexes[1:]):
                iter = self.config[idx]
                for n in range(iter):
                    pn = choice(self.composers[start:end])
                    pn.zone = idx
                    comps.append(pn)
                start = end+1
            shuffle(comps)
            self.generated = comps
        self.already_generated = True

if __name__ == '__main__':
    config = ZonePlaylist.__DEFAULT_ZONE_CONFIG__
    if len(sys.argv) > 1:
        config = sys.argv[1]
    zp = ZonePlaylist.create(config)
    zp.print()
