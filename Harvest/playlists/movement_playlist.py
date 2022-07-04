import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle, choices
from db.db import DbPro
from playlist import Playlist

class MovementPlaylist(Playlist):

    def __init__(self, mov = 'Classical', cache = None):
        super().__init__(cache)
        self.movement = mov
        self.movement_composers = self.load_movement_composers()

    @classmethod
    def create_random_args(cls, cache = None):
        total = 0
        eras = [('Medieval', 29), ('Renaissance', 142),('Baroque', 468), ('Classical', 188), ('Romantic', 488), ('Modernism', 1288), ('Contemporary', 1441)]
        for e,v in eras:
            total +=v 
        weights = [v/float(total) for n,v in eras]
        era = choices(eras, weights = weights)
        return cls(era[0][0], cache)

    def load_movement_composers(self):
        result = []
        for c in self.composers:
            if c.movement_name == self.movement:
                idx = self.zone_lookup(c)
                c.zone=idx
                result.append(c)
        return result

    def generate(self):
        comps = []
        if not self.already_generated:
            prev = None
            for n in range(self.__size__):
                pn = choice(self.movement_composers)
                (pn.log_distance, pn.lin_distance) = self.calc_distance(prev,pn)
                comps.append(pn)
                prev = pn
            #shuffle(comps)
            self.generated = comps
        self.already_generated = True
        
    def print_csv(self, file = sys.stdout):
        super().print_csv(args=self.movement, file = file) 
    
if __name__ == '__main__':
    mov = 'Classical'
    if len(sys.argv) > 1:
        mov = sys.argv[1]
    mp = MovementPlaylist(mov)
    mp.print_csv()
    
    mp.print_stats()
