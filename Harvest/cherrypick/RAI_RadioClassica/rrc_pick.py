import pdb
import os, sys
import re
import datetime as dt

sys.path.append('..')

import common.wikid.wikidata as wd
from common.utilities.path import repo_path
import common.objects as obj
from cherrypick.pdf_source_base import PdfSourceBase
from pathlib import Path
from common.utilities.pdf_file import PDFFile
from common.utilities.string import __UNK__
from rrc_parser.rrc_subdivider import RRCSubdivider

class RRCPick(PdfSourceBase):

    __DEFAULT_RRC_REPO_PATH__ = os.path.join(repo_path, 'RAI-RadioClassica')

    @classmethod
    def manage(cls, repo_dir = __DEFAULT_RRC_REPO_PATH__):
        return super(cls, cls).manage(repo_dir)

    __PROVIDER__ = 'RAIRadioClassica'
    def parse(self):
        for text in self.extract_text():
            rs = RRCSubdivider(text)
            current_date = current_time = None
            current_title = __UNK__
            for o in rs.parse():
                found = not_found = None
                if type(o) is obj.File:
                    current_date = o.date
                elif type(o) is obj.TimeSection:
                    current_time  = o.time
                    current_title = o.title_list
                elif type(o) is obj.Record:
                    comp = o.composer
                    wd_comp = self.retrieve_composer(comp.name)
                    o.composer = wd_comp
                    pdate = RRCPick.process_date(current_date, current_time)
                    o.performance = obj.Performance(pdate, RRCPick.__PROVIDER__, title = current_title)
                    yield o

    @classmethod
    def create_csv(cls, repo_dir = __DEFAULT_RRC_REPO_PATH__):
        return super(cls, cls).create_csv(repo_dir)

    @staticmethod
    def process_date(date, time):
        result = None
        if not date or not time:
            return result
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:8])
        time_start = time[0:6]
        (hours, minutes) = time_start.split(':')
        hours = int(hours)
        minutes = int(minutes)
        seconds = 0
        result = dt.datetime(year, month, day, hours, minutes, seconds).isoformat()
        return result
