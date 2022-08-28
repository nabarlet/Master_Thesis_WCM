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
from common.utilities.string import __UNK__

class MatchNotFound(Exception):
    pass

class StrictPathPlaylist(Playlist):

    def generate(self):
        comps = []
        if not self.already_generated:
            cur = choice(self.zones[0])
            cur.title = self.random_title(cur)
            comps.append(cur)
            try:
                while True:
                    pn = self.next(cur, comps)
                    (pn.log_distance, pn.lin_distance) = self.calc_distance(cur, pn)
                    pn.zone = self.zone_lookup(pn)
                    pn.title = self.generate_title(comps, pn)
                    comps.append(pn)
                    cur = pn
            except MatchNotFound:
                pass # just close the loop
            #shuffle(comps)
            self.generated = comps
        self.already_generated = True

    def generate_title(self, past_comps, cur):
        result = __UNK__
        if len(past_comps) > 0:
            base_query = "SELECT R.title FROM record AS R JOIN record_performance AS RP, composer AS C, performance AS P \
                          WHERE RP.performance_id = P.id AND RP.record_id = R.id AND R.composer_id = C.id AND C.nid = ?"
            per_comp_query = " AND P.id in (SELECT P%d.id FROM record AS R%d JOIN record_performance AS RP%d, composer AS C%d, performance AS P%d \
                              WHERE RP%d.performance_id = P%d.id AND RP%d.record_id = R%d.id AND R%d.composer_id = C%d.id AND C%d.nid = ?)"
            query_tail = ';'
            query = base_query
            values = [cur.nid]
            idx = 2
            for c in past_comps:
                query += (per_comp_query % ((idx,)*12))
                values.append(c.nid)
                idx += 1
            query += query_tail
            results = self.db.query(query, values)
            if results and len(results) > 0:
                result = choice(results)[0]

        if result == __UNK__:
            result = self.random_title(cur)

        return result
        
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
