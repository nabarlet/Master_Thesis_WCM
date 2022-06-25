class PlaylistNode:

    def __init__(self, nid, name, mname, pop):
        self.nid = nid
        self.name = name
        self.movement_name = mname.rstrip()
        self.popvalue = pop
        self.zone = None
        self.crossings = []

    def print(self):
        print("%-36s %-14s - %-16s - zone: %s" % (self.name, '(' + self.nid + ')', self.movement_name, str(self.zone)))

    @classmethod
    def create_from_db(cls, nid, db, pop):
        (nid, name, mname) = cls.load_composer(nid, db)
        return cls(nid, name, mname, pop)

    @staticmethod
    def load_composer(nid, db):
        cquery = "SELECT composer.nid, composer.name, movement.name FROM composer JOIN movement WHERE composer.nid = '%s' AND composer.movement_id = movement.id;" % (nid)
        return db.query(cquery)[0]

    __CACHE_PN_SEPARATOR__ = '|'
    __CACHE_PN_CROSS_SEPARATOR__ = ','
    def save_to_cache(self):
        cps = PlaylistNode.__CACHE_PN_SEPARATOR__
        scross = PlaylistNode.__CACHE_PN_CROSS_SEPARATOR__.join([str(c) for c in self.crossings])
        s = "%s%s%s%s%s%s%s%s%s" % (self.nid, cps, str(self.popvalue), cps, self.name, cps, self.movement_name, cps, scross)
        return s

    @classmethod
    def create_from_cache(cls, string):
        (nid, pop, name, mname, cross) = string.split(PlaylistNode.__CACHE_PN_SEPARATOR__)
        return cls(nid, name, mname, pop)

    @classmethod
    def append_cache_cross_correlations(cls, string, composers):
        from cross_node import CrossNode
        from playlist import Playlist
        (nid, name, mname, cross) = string.split(PlaylistNode.__CACHE_PN_SEPARATOR__)
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
