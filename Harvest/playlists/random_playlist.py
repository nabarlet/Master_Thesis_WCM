import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice
from db.db import DbPro

class RandomPlaylist:

    __DEFAULT_PLAYLIST_SIZE__ = 20
    def __init__(self, size = __DEFAULT_PLAYLIST_SIZE__, db = DbPro()):
        self.db = db
        self.size = size
        self.clear()

    def generate(self):
        if not self.already_generated:
	        table = 'composer'
	        what = 'nid, name'
	        comps = self.db.fetch_all(table, what)
	        for n in range(self.size):
	            self.generated.append(choice(comps))
        self.already_generated = True

    def clear(self):
        self.generated = []
        self.already_generated = False

    def print(self):
        self.generate()
        for n in self.generated:
            print("%s (%s)" % (n[1], n[0]))

    def plot(self):
        pass
