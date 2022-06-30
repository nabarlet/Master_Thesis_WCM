class PlaylistNode:

    def __init__(self, nid, name, mname, pop, cv):
        self.nid = nid
        self.name = name
        self.movement_name = mname.rstrip()
        self.popvalue = pop
        self.cross_value = cv # total number of crossings of this composer with others
        self.zone = None
        self.distance = 0.0
        self.crossings = []

    def print(self):
        print("%-36s %-14s - %-16s - zone: %s" % (self.name, '(' + self.nid + ')', self.movement_name, str(self.zone)))

    def print_csv(self):
        print("\"%s\",\"%s\",%s,%d,%12.10f,%d,%12.10f" % (self.name, self.nid, self.movement_name, self.zone, self.popvalue, self.cross_value, self.distance))

    @classmethod
    def create_from_db(cls, nid, db, pop, value):
        (nid, name, mname) = cls.load_composer(nid, db)
        return cls(nid, name, mname, pop, value)

    @staticmethod
    def load_composer(nid, db):
        cquery = "SELECT composer.nid, composer.name, movement.name FROM composer JOIN movement WHERE composer.nid = '%s' AND composer.movement_id = movement.id;" % (nid)
        return db.query(cquery)[0]

    __CACHE_PN_SEPARATOR__ = '|'
    __CACHE_PN_CROSS_SEPARATOR__ = ','
    def save_to_cache(self):
        cps = PlaylistNode.__CACHE_PN_SEPARATOR__
        scross = PlaylistNode.__CACHE_PN_CROSS_SEPARATOR__.join([str(c) for c in self.crossings])
        s = "%s%s%s%s%d%s%s%s%s%s%s" % (self.nid, cps, str(self.popvalue), cps, self.cross_value, cps, self.name, cps, self.movement_name, cps, scross)
        return s

    @classmethod
    def create_from_cache(cls, string):
        (nid, pop, cv, name, mname, cross) = string.split(PlaylistNode.__CACHE_PN_SEPARATOR__)
        return cls(nid, name, mname, float(pop), int(cv))

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
