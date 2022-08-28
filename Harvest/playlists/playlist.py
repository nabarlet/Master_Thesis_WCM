import pdb
import sys, os
import math
import re
import numpy as np
import datetime as dt
from   random import choice

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from common.utilities.composer_plot import ComposerPlot
from common.utilities.wcm_math import exp_decile
from common.utilities.string import __UNK__
from common.objects.timeline import TimeLine
from db.db import DbPro
from playlist_node import PlaylistNode
from cross_node import CrossNode

class PureVirtualMethodCalled(Exception):
    pass
    
class PlaylistStats:
    
    def __init__(self, playlist):
        self.playlist = playlist
        self.calc_stats()
        
    def calc_stats(self):
        self.eras_dist = self.eras_dist_calc()
        self.zones_dist = self.zones_dist_calc()
        self.composers_list = self.composers_list_calc()
        self.pop_avg = self.pop_avg_calc()
        self.pop_median = self.pop_median_calc()
        self.distance_avg = self.distance_avg_calc()
    
    def print_stats(self, file=sys.stderr):
        self.playlist.print_csv(file = file)
        print('Size of playlist: ' + str(len(self.playlist.generated)), file = file)
        print('Eras: ' + str(self.eras_dist), file=file)
        print('Zones: ' + str(self.zones_dist),file=file)
        print('Composers: ' + str(self.composers_list), file=file)
        print('Pop_Average: ' + str(self.pop_avg), file=file)
        print('Pop_Median: ' + str(self.pop_median), file=file)
        print('Average distance (log,lin): ' + str(self.distance_avg), file=file)
    
    def build_stats(self, d):
        for k,v in d.items():
            d[k] = (v/(self.playlist.size()))*100.0
        return sorted(d.items(),key=lambda x:x[1], reverse=True)
           
    def eras_dist_calc(self):
        tl = TimeLine.create()
        result = {k:0 for k in tl.keys()}
        max_value = 0        
        for pn in self.playlist.run():
            result[pn.movement_name] += 1
        return self.build_stats(result)
        
    def composers_list_calc(self):        
        result = {pn.name:0 for pn in self.playlist.run()}
        for pn in self.playlist.run():
            result[pn.name] += 1
        return self.build_stats(result)
        
    def zones_dist_calc(self):        
        result = {pn.zone:0 for pn in self.playlist.run()}
        for pn in self.playlist.run():
            result[pn.zone] += 1
        return self.build_stats(result) 
        
    def pop_avg_calc(self):
        result = 0
        for pn in self.playlist.run():
            result += pn.popvalue
        result /= (self.playlist.size())
        return result
        
    def pop_median_calc(self):
        sort_result = sorted([pn.popvalue for pn in self.playlist.run()])
        sz = len(sort_result)
        idx = int((sz+1)/2.0)-1
        result = None
        if (sz%2) > 0:
            result = sort_result[idx]
        else:
            prev = sort_result[idx]
            next = sort_result[idx+1]
            result = (prev + next)/2.0
        return result
        
    def distance_avg_calc(self):
        result_log = 0
        result_lin = 0
        for pn in self.playlist.run():
            result_log += pn.log_distance
            result_lin += pn.lin_distance
        result_log /= (self.playlist.size())
        result_lin /= (self.playlist.size())
        return (result_log, result_lin)
        
        
class Playlist:

    __DEFAULT_PLAYLIST_SIZE__ = 10
    def __init__(self, cache = None, size = __DEFAULT_PLAYLIST_SIZE__, db = DbPro()):
        self.db = db
        self.__size__ = size
        self.composers = self.load_composers(cache)
        self.zones = self.subdivide_in_zones()
        self.clear()
        
    @classmethod
    def create_random_args(cls, cache = None):
        return cls(cache)
        
    def size(self):
        self.generate()
        return len(self.generated)

    __PLAYLIST_CACHE_NAME__ = os.path.join(mypath, '__playlist_cache__')
    def load_composers(self, cache = None):
        """
            load_composers()

            returns the sorted arrays of PlaylistNodes objects each
            representing a composer along with all her/his cross-relationships
            with other composers. This requires a two-pass process first
            loading all the composers and then creating the
            cross-relationships
        """
        if cache:
            result = cache
        else:
            result = Playlist.load_composers_from_cache()
        if len(result) == 0:
            cp = ComposerPlot()
            skeys = cp.sorted_keys
            with open(Playlist.__PLAYLIST_CACHE_NAME__, 'w') as file:
                for key, coeff, value in skeys:
                    if(value>0):
                        pn = PlaylistNode.create_from_db(key, self.db, coeff, value)
                        result.append(pn)
                for pn in result:
                    for cross in cp.cross_lookup(pn.nid):
                        cpn = Playlist.lookup(cross.col_nid, result)
                        pn.crossings.append(CrossNode(cpn, cross.conditioned_value, cross.value()))
                    if len(pn.crossings) > 0:
                        pn.crossings = sorted(pn.crossings, key=lambda x:x.log_distance, reverse=True)
                        cache_string = pn.save_to_cache()
                        print(cache_string, file=file)
        return result

    @staticmethod
    def load_composers_from_cache():
        result = []
        if os.path.exists(Playlist.__PLAYLIST_CACHE_NAME__):
            with open(Playlist.__PLAYLIST_CACHE_NAME__, 'r') as file:
                for line in file:
                    result.append(PlaylistNode.create_from_cache(line))
                file.seek(0)
                for line in file:
                    PlaylistNode.append_cache_cross_correlations(line, result)
        return result

    def generate(self):
        raise PureVirtualMethodCalled
        self.already_generated = True

    def random_title(self, pn):
        """
            random_title(playlist_node)

            generates a random title among the composer's titles available
        """
        result = __UNK__
        query = "SELECT R.title FROM record as R JOIN composer AS C WHERE C.nid = ? AND R.composer_id = C.id"
        values = (pn.nid, )
        results = self.db.query(query, values)
        result  = choice(results)[0]
        return result

    def generate_title(self, prev, nxt):
        """
            generate_title(prev, next)

            generates a title for the next composer based on the possible
            existing connection between the previous one and the next. This
            implies that both have appeared at least once on a real playlist
            somewhere. If no connection is found, then a random title of the
            next composer is chosen.
        """
        result = __UNK__
        if prev:
            query = "SELECT R.title FROM record AS R JOIN record_performance AS RP, composer AS C, performance AS P \
                            WHERE RP.performance_id = P.id AND RP.record_id = R.id AND R.composer_id = C.id AND C.nid = ? \
                            AND P.id in (SELECT P2.id FROM record AS R2 JOIN record_performance AS RP2, composer AS C2, performance AS P2 \
                            WHERE RP2.performance_id = P2.id AND RP2.record_id = R2.id AND R2.composer_id = C2.id AND C2.nid = ?);"
            values = (nxt.nid, prev.nid,)
            results = self.db.query(query, values)
            if results and len(results) > 0:
                result = choice(results)[0]

        if result == __UNK__:
            result = self.random_title(nxt)

        return result

    @staticmethod
    def calc_distance(a, b):
        """
            calc_distance(a, b)

            calculates the distance between composer A and composer B
            by checking the position of composer B in the crossings of
            composer A. Returns 0 if no crossing is found.
        """
        result = (0.0, 0)
        if a:
            for c in a.crossings:
                if b.nid == c.node.nid:
                    result = (c.log_distance, c.lin_distance)
        return result

    def clear(self):
        self.generated = []
        self.already_generated = False

    def print(self):
        self.generate()
        for pn in self.generated:
            pn.print()

    def header(self, args):
        return "=== %s (%s) (%s) ===" % (self.__class__.__name__, dt.datetime.now().isoformat(), args)

    def print_csv(self, args = '', file = sys.stdout):
        self.generate()
        print(file = file) # precede header with a newline
        print(self.header(args), file = file)
        print("name,nid,movement,zone,pop_value,crossings,log_d,lin_d", file = file)
        for pn in self.generated:
            pn.print_csv(file = file)

    def plot(self):
        pass

    @staticmethod
    def calc_distance(a, b):
        """
            calc_distance(a, b)

            calculates the distance between composer A and composer B
            by checking the position of composer B in the crossings of
            composer A. Returns 0 if no crossing is found.
        """
        result = (0.0, 0)
        if a:
            for c in a.crossings:
                if b.nid == c.node.nid:
                    result = (c.log_distance, c.lin_distance)
        return result

    def clear(self):
        self.generated = []
        self.already_generated = False

    def print(self):
        self.generate()
        for pn in self.generated:
            pn.print()

    def header(self, args):
        return "=== %s (%s) (%s) ===" % (self.__class__.__name__, dt.datetime.now().isoformat(), args)

    def print_csv(self, args = '', file = sys.stdout):
        self.generate()
        print(file = file) # precede header with a newline
        print(self.header(args), file = file)
        print("name,nid,movement,zone,pop_value,crossings,log_d,lin_d", file = file)
        for pn in self.generated:
            pn.print_csv(file = file)

    def plot(self):
        pass

    @staticmethod
    def lookup(nid, composers):
        """
            lookup(nid, composers)

            expects a nid and a composers list as input and returns in any
            case a PlaylistNode as output.
            This must be a static function because it assumes that the
            composers list is already existing, but it is also called during
            initialization (when self.composers does not yet exist)
        """
        result = None
        for pn in composers:
            if pn.nid == nid:
                result = pn
                break
        return result

    __ZONE_0_SIZE__ = 30
    def subdivide_in_zones(self):
        result = []
        subdiv = exp_decile(self.composers, Playlist.__ZONE_0_SIZE__)
        start = subdiv[0]
        idx = 0
        for end in subdiv[1:]:
            zcomps=self.composers[start:end]
            for zc in zcomps:
                zc.zone = idx
            result.append(zcomps)
            start = end
            idx += 1
        return result

    def zone_lookup(self, pn):
        result = None
        for idx, zone in enumerate(self.zones):
            if pn in zone:
                result = idx
                break
        return result
        
    def calc_stats(self):
        self.generate()
        result = PlaylistStats(self)
        return result
        
    def print_stats(self, file=sys.stderr):
        cs = self.calc_stats()
        cs.print_stats(file)
        
    def run(self):
        self.generate()
        for pn in self.generated:
            yield pn
