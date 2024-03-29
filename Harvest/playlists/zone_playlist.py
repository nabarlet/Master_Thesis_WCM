import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from playlist import Playlist
from common.utilities.wcm_math import decile, exp_decile
from utilities.plugs import exclusive_random

class ZonePlaylist(Playlist):

    def __init__(self, config, cache = None):
        super().__init__(cache)
        self.config = config

    __DEFAULT_ZONE_CONFIG__ = '1,1,1,1,1,1,1,1,1,1'
    @classmethod
    def create(cls, config_string = __DEFAULT_ZONE_CONFIG__, cache = None):
        result = config_string.split(',')
        result = [int(n) for n in result]
        return cls(result, cache)

    @classmethod
    def create_random_args(cls, cache = None):
        return cls.create(ZonePlaylist.__DEFAULT_ZONE_CONFIG__, cache)

    def generate(self):
        if not self.already_generated:
            comps = []
            for idx, z in enumerate(self.zones):
                iter = self.config[idx]
                already_chosen = []
                prev = None
                for n in range(iter):
                    pn = exclusive_random(z, already_chosen)
                    pn.zone = idx
                    pn.title = self.generate_title(prev, pn)
                    already_chosen.append(pn)
                    comps.append(pn)
                    prev = pn
            # shuffle(comps)
            self.generated = comps
        self.already_generated = True

if __name__ == '__main__':
    config = ZonePlaylist.__DEFAULT_ZONE_CONFIG__
    if len(sys.argv) > 1:
        config = sys.argv[1]
    zp = ZonePlaylist.create(config)
    zp.print_csv(config)
