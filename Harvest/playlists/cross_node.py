import pdb
from playlist_node import PlaylistNode

class CrossNode:

    def __init__(self, pn, how_many_log, how_many_lin):
        self.node = pn                 # This should be a playlist node
        self.log_distance = how_many_log
        self.lin_distance = how_many_lin

    def __str__(self):
        return "%s(%.6g:%3.1f)" % (self.node.nid, self.log_distance,self.lin_distance)

    @classmethod
    def create_from_string(cls, string, composers):
        from playlist import Playlist
        (cnid, how_many) = string.split('(')
        pn = Playlist.lookup(cnid, composers)
        (log, lin) = how_many.split(':')
        lin = lin.rstrip(')')
        return cls(pn, float(log), float(lin))

    def match(self, rng):
        result = False
        if self.log_distance >= rng[0] and self.log_distance <= rng[1]:
            result = True
        return result
