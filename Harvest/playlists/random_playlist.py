import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice
from db.db import DbPro
from playlist import Playlist

class RandomPlaylist(Playlist):

    def generate(self):
        if not self.already_generated:
            cur = None
            for n in range(self.__size__):
                pn = choice(self.composers)
                if cur:
                    (pn.log_distance, pn.lin_distance) = self.calc_distance(cur, pn)
                else:
                    (pn.log_distance, pn.lin_distance) = (0.0, 0.0)
                pn.zone = self.zone_lookup(pn)
                self.generated.append(pn)
                cur = pn
        self.already_generated = True

if __name__ == '__main__':
    rp = RandomPlaylist()
    rp.print_csv()
    
    rp.print_stats()
