import sys, os
import pdb

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, '..', 'cherrypick'))

from common.utilities.string import __UNK__

class PlaylistNode:

    def __init__(self, nid, name, mname, pop, cv):
        self.nid = nid
        self.name = name
        self.title = __UNK__
        self.movement_name = mname.rstrip()
        self.popvalue = pop
        self.cross_value = cv # total number of crossings of this composer with others
        self.zone = None
        self.log_distance = 0.0
        self.lin_distance = 0
        self.crossings = []

    def print(self, file=sys.stdout):
        print("%-36s %-14s - %-16s - zone: %s - title: \"%s\"" % (self.name, '(' + self.nid + ')', self.movement_name, str(self.zone), self.title), file=file)

    def print_csv(self, file=sys.stdout):
        if self.zone == None:
            self.zone = -1
        print("\"%s\",\"%s\",%s,%d,%.6g,%d,%.6g,%3.1f,\"%s\"" % (self.name, self.nid, self.movement_name, self.zone, self.popvalue, self.cross_value, self.log_distance, self.lin_distance, self.title), file=file)

    @classmethod
    def create_from_db(cls, nid, db, pop, value):
        (nid, name, mname) = cls.load_composer(nid, db)
        return cls(nid, name, mname, pop, value)

    @staticmethod
    def load_composer(nid, db):
        cquery = "SELECT C.nid, C.name, M.name FROM composer AS C JOIN movement AS M WHERE C.nid = ? AND C.movement_id = M.id;"
        values = (nid,)
        return db.query(cquery, values)[0]

    __CACHE_PN_SEPARATOR__ = '|'
    __CACHE_PN_CROSS_SEPARATOR__ = ','
    def save_to_cache(self):
        cps = PlaylistNode.__CACHE_PN_SEPARATOR__
        scross = PlaylistNode.__CACHE_PN_CROSS_SEPARATOR__.join([str(c) for c in self.crossings])
        s = "%s%s%.6g%s%3.1f%s%s%s%s%s%s" % (self.nid, cps, self.popvalue, cps, self.cross_value, cps, self.name, cps, self.movement_name, cps, scross)
        return s

    @classmethod
    def create_from_cache(cls, string):
        (nid, pop, cv, name, mname, cross) = string.split(PlaylistNode.__CACHE_PN_SEPARATOR__)
        return cls(nid, name, mname, float(pop), float(cv))

    @classmethod
    def append_cache_cross_correlations(cls, string, composers):
        from cross_node import CrossNode
        from playlist import Playlist
        (nid, pop, cv, name, mname, cross) = string.split(PlaylistNode.__CACHE_PN_SEPARATOR__)
        cross = cross.rstrip()
        result = Playlist.lookup(nid, composers)
        for c in cross.split(PlaylistNode.__CACHE_PN_CROSS_SEPARATOR__):
            if c:
                result.crossings.append(CrossNode.create_from_string(c, composers))
        return result

    def lookup_cross_range(self, range):
        result = []
        for other in self.crossings:
            if other.match(range):
                result.append(other)
        return result

    def lookup_cross_range_and_zone(self, range, zone_array):
        result = []
        for other in self.crossings:
            if other.match(range) and other.node in zone_array:
                result.append(other)
        return result
