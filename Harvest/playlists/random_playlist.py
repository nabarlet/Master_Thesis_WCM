import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from random import choice
from db.db import DbPro
from playlist import Playlist

class RandomPlaylist(Playlist):

    def generate(self):
        if not self.already_generated:
	        for n in range(self.size):
	            self.generated.append(choice(self.composers))
        self.already_generated = True
