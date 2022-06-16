import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

import numpy as np
from random import choice, shuffle
from db.db import DbPro
from zone_playlist import ZonePlaylist
from common.utilities.wcm_math import exp_decile

class ExpZonePlaylist(ZonePlaylist):

    def generate(self):
        if not self.already_generated:
            d_indexes = exp_decile(len(self.composers), 20)
            np.append(d_indexes, len(self.composers)-1)
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
    zp = ExpZonePlaylist.create(config)
    zp.print()
