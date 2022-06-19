import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from playlist import Playlist

class MovementPlaylist(Playlist):

    def __init__(self, mov = 'Classical'):
        super().__init__()
        self.movement = mov
        self.movement_composers = self.load_movement_composers()

    def load_movement_composers(self):
        result = []
        for c in self.composers:
            if c.movement_name == self.movement:
                result.append(c)
        return result

    def generate(self):
        comps = []
        if not self.already_generated:
            for n in range(self.size):
                pn = choice(self.movement_composers)
                pn.zone = self.zone_lookup(pn)
                comps.append(pn)
            shuffle(comps)
            self.generated = comps
        self.already_generated = True

if __name__ == '__main__':
    mov = 'Classical'
    if len(sys.argv) > 1:
        mov = sys.argv[1]
    mp = MovementPlaylist(mov)
    mp.print()
