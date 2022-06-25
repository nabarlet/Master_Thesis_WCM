import pdb
import os,sys
import re
import csv
import datetime as dt

root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root_path)

import common.wikid.wikidata as wd
from common.utilities.path import repo_path
from common.wikid.sparql import sparql_composer
from common.objects import Composer
from cherrypick.csv_source_base import CsvSourceBase
from bbc3_base import BBC3Base
from bbc3_schedule import BBC3Schedule

class BBC3Pick(CsvSourceBase):

    __DEFAULT_BBC3_REPO_PATH__ = os.path.join(repo_path, 'BBC3')

    cache = []

    def __init__(self, file):
        super(BBC3Pick, self).__init__(file)
        self.schedule = BBC3Schedule()

    @classmethod
    def manage(cls, repo_dir = __DEFAULT_BBC3_REPO_PATH__):
        return super(BBC3Pick, cls).manage(repo_dir)

    @classmethod
    def create_csv(cls, repo_dir = __DEFAULT_BBC3_REPO_PATH__):
        for coll in cls.manage(repo_dir):
            extractor = coll.format_extractor()
            for comp in extractor():
                found = not_found = None
                if comp.nid and comp.birth:
                    found = comp
                else:
                    not_found = comp
                yield found, not_found

    def extractor_version_0(self):
        with open(self.filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            lineno = 0
            for row in reader:
                lineno += 1
                movement = None
                if len(row) == 5:
                    (name, birth, death, title, perf_date) = row
                elif len(row) == 6:
                    (name, birth, death, movement, title, perf_date) = row
                else:
                    print("ValueError: wrong values to unpack: %d (file: %s, line: %d). Skipping..." % (len(row), os.path.basename(self.filename), lineno), file=sys.stderr)
                    continue
                try:
                    qperf_date = self.schedule.quantize_date(BBC3Base.process_date(perf_date)).isoformat()
                except ValueError as e:
                    print("row: %s generates date error (ValueError)" % (row), file=sys.stderr)
                    raise ValueError(e)
                key = str(perf_date)
                if not key in BBC3Pick.cache:
                    BBC3Pick.cache.append(key)
                    comp = self.retrieve_composer(name)
                    if comp:
                        comp.perf_date = qperf_date
                        yield comp
                else:
                    print("extractor 0 file %s: found key %s in cache... not appending" %(os.path.basename(self.filename), key), file=sys.stderr)

    def extractor_version_1(self):
        with open(self.filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                (nid, name, birth, death, movement, perf_date) = row
                key = str(perf_date)
                qperf_date = self.schedule.quantize_date(BBC3Base.process_date(perf_date))
                if not key in BBC3Pick.cache:
                    BBC3Pick.cache.append(key)
                    comp = Composer(name, birth, death, movement, qperf_date, nid)
                    yield comp
                else:
                    print("extractor 1 file %s: found key %s in cache... not appending" % (os.path.basename(self.filename), key), file=sys.stderr)

    def format_extractor(self):
        re_Q = re.compile('\AQ\d+')
        extractor = None
        with open(self.filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            #
            # skip header
            #
            reader 
            for testrow in reader:
                if re_Q.match(testrow[0]):
                    extractor = self.extractor_version_1
                else:
                    extractor = self.extractor_version_0
                break
        return extractor
