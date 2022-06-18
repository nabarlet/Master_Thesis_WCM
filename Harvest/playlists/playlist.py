import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from common.utilities.composer_plot import ComposerPlot
from db.db import DbPro

class CrossNode:

    def __init__(self, cnid, how_many):
        self.cross_nid = cnid
        self.how_many_times = how_many

    def __str__(self):
        return "%s(%d)" % (self.cross_nid, self.how_many_times)

    @classmethod
    def create_from_string(cls, string):
        (cnid, how_many) = string.split('(')
        how_many.rstrip(')')
        return cls(cnid, how_many)

class PlaylistNode:

    def __init__(self, nid, name, mname):
        self.nid = nid
        self.name = name
        self.movement_name = mname.rstrip()
        self.zone = None
        self.crossings = []

    def print(self):
        print("%-36s %-14s - %-16s - zone: %s" % (self.name, '(' + self.nid + ')', self.movement_name, str(self.zone)))

    @classmethod
    def create_from_db(cls, nid, db):
        (nid, name, mname) = cls.load_composer(nid, db)
        return cls(nid, name, mname)

    @staticmethod
    def load_composer(nid, db):
        cquery = "SELECT composer.nid, composer.name, movement.name FROM composer JOIN movement WHERE composer.nid = '%s' AND composer.movement_id = movement.id;" % (nid)
        return db.query(cquery)[0]

    __CACHE_PN_SEPARATOR__ = '|'
    __CACHE_PN_CROSS_SEPARATOR__ = ','
    def save_to_cache(self):
        cps = PlaylistNode.__CACHE_PN_SEPARATOR__
        scross = PlaylistNode.__CACHE_PN_CROSS_SEPARATOR__.join([str(c) for c in self.crossings])
        s = "%s%s%s%s%s%s%s" % (self.nid, cps, self.name, cps, self.movement_name, cps, scross)
        return s

    @classmethod
    def create_from_cache(cls, string):
        (nid, name, mname, cross) = string.split(PlaylistNode.__CACHE_PN_SEPARATOR__)
        result = cls(nid, name, mname)
        cross = cross.rstrip()
        for c in cross.split(PlaylistNode.__CACHE_PN_CROSS_SEPARATOR__):
            if c:
                result.crossings.append(CrossNode.create_from_string(c))
        return result


class PureVirtualMethodCalled(Exception):
    pass

class Playlist:

    __DEFAULT_PLAYLIST_SIZE__ = 20
    def __init__(self, size = __DEFAULT_PLAYLIST_SIZE__, db = DbPro()):
        self.db = db
        self.size = size
        self.composers = self.load_composers()
        self.clear()

    __PLAYLIST_CACHE_NAME__ = os.path.join(mypath, '__playlist_cache__')
    def load_composers(self):
        result = self.load_composers_from_cache()
        if len(result) == 0:
            cp = ComposerPlot()
            skeys = cp.sorted_keys
            with open(Playlist.__PLAYLIST_CACHE_NAME__, 'w') as file:
                for key, coeff in skeys:
                    pn = PlaylistNode.create_from_db(key, self.db)
                    for cross in cp.cross_lookup(key):
                        pn.crossings.append(CrossNode(cross.col_nid, cross.value))
                    cache_string = pn.save_to_cache()
                    print(cache_string, file=file)
                    result.append(pn)
        return result

    def load_composers_from_cache(self):
        result = []
        if os.path.exists(Playlist.__PLAYLIST_CACHE_NAME__):
            with open(Playlist.__PLAYLIST_CACHE_NAME__, 'r') as file:
                for line in file:
                    result.append(PlaylistNode.create_from_cache(line))
        return result

    def generate(self):
        raise PureVirtualMethodCalled
        self.already_generated = True

    def clear(self):
        self.generated = []
        self.already_generated = False

    def print(self):
        self.generate()
        for pn in self.generated:
            pn.print()

    def plot(self):
        pass

