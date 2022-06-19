from playlist_node import PlaylistNode

class CrossNode:

    def __init__(self, pn, how_many):
        self.node = pn                 # This should be a playlist node
        self.how_many_times = how_many

    def __str__(self):
        return "%s(%10.8f)" % (self.node.nid, self.how_many_times)

    @classmethod
    def create_from_string(cls, string, composers):
        from playlist import Playlist
        (cnid, how_many) = string.split('(')
        pn = Playlist.lookup(cnid, composers)
        how_many = how_many.rstrip(')')
        return cls(pn, float(how_many))

    def match(self, rng):
        result = False
        if self.how_many_times >= rng[0] and self.how_many_times < rng[1]:
            result = True
        return result
