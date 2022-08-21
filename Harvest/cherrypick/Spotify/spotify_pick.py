import pdb
import os,sys
import re
import csv

root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root_path)

from common.utilities.path import repo_path
from cherrypick.csv_source_base import CsvSourceBase

class SpotifyPick(CsvSourceBase):

    __DEFAULT_Spotify_REPO_PATH__ = os.path.join(repo_path, 'Spotify')

    __PROVIDER__ = 'Spotify'
    def __init__(self, file, provider = __PROVIDER__):
        super(SpotifyPick, self).__init__(file, provider)

    @classmethod
    def manage(cls, repo_dir = __DEFAULT_Spotify_REPO_PATH__):
        return super(SpotifyPick, cls).manage(repo_dir, SpotifyPick.__PROVIDER__)

    @classmethod
    def create_csv(cls, repo_dir = __DEFAULT_Spotify_REPO_PATH__):
        for coll in cls.manage(repo_dir):
            for comp in coll.extract():
                found = not_found = None
                if comp.nid and comp.birth:
                    found = comp
                else:
                    not_found = comp
                yield found, not_found

    def extract(self):
        with open(self.filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = '\t')
            for row in reader:
                if row[0] == 'genre':  # this is the header
                    continue
                (playlist, feat, sp_id, comp, title, isrc, pop) = row
                auth_comp = self.retrieve_composer(comp)
                auth_comp.perf_date = playlist
                yield auth_comp
