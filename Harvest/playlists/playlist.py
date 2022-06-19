import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from common.utilities.composer_plot import ComposerPlot
from db.db import DbPro
from playlist_node import PlaylistNode
from cross_node import CrossNode

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
        """
            load_composers()

            returns the sorted arrays of PlaylistNodes objects each
            representing a composer along with all her/his cross-relationships
            with other composers. This requires a two-pass process first
            loading all the composers and then creating the
            cross-relationships
        """
        result = self.load_composers_from_cache()
        if len(result) == 0:
            cp = ComposerPlot()
            skeys = cp.sorted_keys
            with open(Playlist.__PLAYLIST_CACHE_NAME__, 'w') as file:
                for key, coeff in skeys:
                    pn = PlaylistNode.create_from_db(key, self.db)
                    result.append(pn)
                for pn in result:
                    for cross in cp.cross_lookup(pn.nid):
                        cpn = Playlist.lookup(cross.col_nid, result)
                        pn.crossings.append(CrossNode(cpn, cross.conditioned_value))
                    pn.crossings = sorted(pn.crossings, key=lambda x:x.how_many_times, reverse=True)
                    cache_string = pn.save_to_cache()
                    print(cache_string, file=file)
        return result

    def load_composers_from_cache(self):
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

    def clear(self):
        self.generated = []
        self.already_generated = False

    def print(self):
        self.generate()
        for pn in self.generated:
            pn.print()

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
