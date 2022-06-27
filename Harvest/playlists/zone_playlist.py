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
from utilities.plugs import exclusive_random

class ZonePlaylist(Playlist):

    def __init__(self, config):
        super().__init__()
        self.config = config

    __DEFAULT_ZONE_CONFIG__ = '1,1,1,1,1,1,1,2,2,4,5'
    @classmethod
    def create(cls, config_string = __DEFAULT_ZONE_CONFIG__):
        result = config_string.split(',')
        result = [int(n) for n in result]
        return cls(result)

    def generate(self):
        if not self.already_generated:
            dataset = [pn.cross_value for pn in self.composers]
            d_indexes = decile(dataset, 10)
            start = d_indexes[0]
            comps = []
            for idx, end in enumerate(d_indexes[1:]):
                iter = self.config[idx]
                already_chosen = []
                for n in range(iter):
                    pn = exclusive_random(self.composers[start:end], already_chosen)
                    pn.zone = idx
                    already_chosen.append(pn)
                    comps.append(pn)
                start = end+1
            # shuffle(comps)
            self.generated = comps
        self.already_generated = True

if __name__ == '__main__':
    config = ZonePlaylist.__DEFAULT_ZONE_CONFIG__
    if len(sys.argv) > 1:
        config = sys.argv[1]
    zp = ZonePlaylist.create(config)
    zp.print_csv()
