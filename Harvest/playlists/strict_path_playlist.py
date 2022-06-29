import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice, shuffle
from db.db import DbPro
from playlist import Playlist
from utilities.plugs import exclusive_random

class MatchNotFound(Exception):
    pass

class StrictPathPlaylist(Playlist):

    def generate(self):
        comps = []
        if not self.already_generated:
            cur = choice(self.zones[0])
            comps.append(cur)
            try:
                while True:
                    pn = self.next(cur, comps)
                    pn.distance = self.calc_distance(cur, pn)
                    pn.zone = self.zone_lookup(pn)
                    comps.append(pn)
                    cur = pn
            except MatchNotFound:
                pass # just close the loop
            #shuffle(comps)
            self.generated = comps
        self.already_generated = True
        
    def next(self, cur, already_found):
        possibilities = self.find_possibilities(cur, already_found, 0)
        if len(possibilities) < 1:
            raise MatchNotFound

        result = exclusive_random(possibilities,already_found)
        return result   

    def find_possibilities(self, cur, already_found, attempt):
        result = None
        temp = cur.crossings
        possibilities = []
        for other in temp:
            match = True
            for pn in already_found:
                if not self.cross_lookup(cur, pn):
                    match = False
            if match:
                possibilities.append(other.node)

        if len(possibilities) < 1 and attempt < 10:
            idx = -2
            if len(already_found) < 3:
                idx = 0
            prev = already_found[idx]
            possibilities = self.find_possibilities(prev, already_found, attempt+1)

        return possibilities

    def cross_lookup(self, cur, other):
        result = False
        for cn in other.crossings:
            if cur.nid == cn.node.nid:
                result = True
        return result
                

if __name__ == '__main__':
    mp = StrictPathPlaylist()
    mp.print_csv()
