import pdb
import os,sys
import re
import csv

root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root_path)

import common.wikid.wikidata as wd
from common.utilities.path import repo_path
from common.wikid.sparql import sparql_composer
from common.objects import Composer
from cherrypick.csv_source_base import CsvSourceBase

class JMMPick(CsvSourceBase):

    __DEFAULT_JMM_REPO_PATH__ = os.path.join(repo_path, 'JMM')

    def __init__(self, file):
        super(JMMPick, self).__init__(file)

    @classmethod
    def manage(cls, repo_dir = __DEFAULT_JMM_REPO_PATH__):
        return super(JMMPick, cls).manage(repo_dir)

    @classmethod
    def create_csv(cls, repo_dir = __DEFAULT_JMM_REPO_PATH__):
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
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'fecha':  # this is the header
                    continue
                (perf_date, concert, course, title, comp_string, typology) = row
                composers = comp_string.split(', ')
                for name in composers:
                    comp = wd.retrieve_composer(name)
                    comp.perf_date = perf_date
                    yield comp
