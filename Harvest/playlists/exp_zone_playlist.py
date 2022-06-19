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
            comps = []
            for idx, zone in enumerate(self.zones):
                iter = self.config[idx]
                for n in range(iter):
                    pn = choice(zone)
                    pn.zone = idx
                    comps.append(pn)
            shuffle(comps)
            self.generated = comps
        self.already_generated = True

if __name__ == '__main__':
    config = ZonePlaylist.__DEFAULT_ZONE_CONFIG__
    if len(sys.argv) > 1:
        config = sys.argv[1]
    zp = ExpZonePlaylist.create(config)
    zp.print()
