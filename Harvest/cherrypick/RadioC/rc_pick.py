import pdb
import os, sys
sys.path.extend([os.path.join(os.path.dirname(__file__),'..'), os.path.join(os.path.dirname(__file__), '..', 'common')])
import re

import common.wikid.wikidata as wd
from utilities.path import root_path
from utilities.pdf_file import PDFFile
from utilities.string import string_similarity
from cherrypick.pdf_source_base import PdfSourceBase
from pathlib import Path
from rc_parser.rc_lex import RCLexer
from utilities.date import spanish_date_conditioner

class EndOfHeaderNotFound(Exception):
    pass

class RCPick(PdfSourceBase):

    __DEFAULT_RC_REPO_PATH__ = os.path.join(os.path.dirname(__file__), *['..']*3, 'Repo', 'RadioC')

    @classmethod
    def manage(cls, repo_dir = __DEFAULT_RC_REPO_PATH__):
        return super(cls, cls).manage(repo_dir)

    def extract_text_from_pdf(self):
        text = ""
        for t in self.pdf.readpage():
            text += t
        return text

    __RC_COMPOSER_LINE_RE__       = u'[A-ZÀ-Ý][A-ZÀ-Ý\.,\s\/\-]{4,}:'
    def extract_composer(self):
        for cl, date, time in self.find_composer_lines():
            re_comp = re.compile(RCPick.__RC_COMPOSER_LINE_RE__, re.UNICODE)
            comps = re_comp.findall(cl)
            comps = [c.rstrip(':') for c in comps]
            for c in comps:
                yield c, date, time

    def parse(self):
        re_s = re.compile('\s*\/\s*')
        for this_comp, date, time in self.extract_composer():
            this_comp = this_comp.rstrip('\n')
            wd_comp = self.retrieve_composer(this_comp)
            if wd_comp:
                wd_comp.perf_date = self.extract_date(date, time)
                yield wd_comp

    __RC_HEADER_RE__              = "\A(LUNES|MARTES|MIÉRCOLES|JUEVES|VIERNES|SÁBADO|DOMINGO)\s+\d{1,2}\s*\Z"
    __RC_COMPOSER_LINE_START_RE__ = '\A[A-Z]{2,}:'
    __RC_COMPOSER_LINE_END_RE__   = '\A\d{2}\.\d{2}\s+'
    def find_composer_lines(self):
        """
            find_composer_lines():

            it scans for lines which start with a capital letter and it stops
            scanning when it encounters a string that resembles a time
            (because that will finish the composer lines).
            Finally it'll keep only the lines that contain capital letters
            and yield them to the caller.
        """
        body = self.gobble_header()
        re_start = re.compile(RCPick.__RC_COMPOSER_LINE_START_RE__, re.I)
        re_end   = re.compile(RCPick.__RC_COMPOSER_LINE_END_RE__, re.I)
        re_comp  = re.compile(RCPick.__RC_COMPOSER_LINE_RE__, re.I)
        re_date  = re.compile(RCPick.__RC_HEADER_RE__, re.I)
        idx_start = None
        comp_line = None
        date_found = None
        time_found = '00.00'
        for idx,l in enumerate(body):
            if re_date.search(l):
                date_found = l
                continue
            if re_end.search(l):
                idx_start = None
                if comp_line and len(comp_line) > 0:
                    full_comp_line = ''.join(comp_line)
                    if len(re_comp.findall(full_comp_line)) > 0:
                        yield full_comp_line, date_found, time_found
                comp_line = None
                time_found = l
            if re_start.search(l):
                idx_start = idx
                comp_line = []
            if idx_start:
                comp_line.append(l.rstrip())
                        

    def gobble_header(self):
        """
            gobble_header()

            We have to skip all the lines until we find lines that
            start with some day of the week in spanish all capital letters.
            There starts the actual body and we start looking for composer
            lines.
        """
        rgobble = re.compile(RCPick.__RC_HEADER_RE__, re.I)
        result = self.extract_text_from_pdf().split("\n")
        start_line = None
        for idx,l in enumerate(result):
            if rgobble.search(l):
                start_line = idx
                break
        if not start_line:
            raise EndOfHeaderNotFound(os.path.basename(self.filename))
        return result[start_line:]

    @classmethod
    def create_csv(cls, repo_dir = __DEFAULT_RC_REPO_PATH__):
        return super().create_csv(repo_dir)

    def inspect(self):
        for comp, date, time in self.extract_composer():
            yield comp

    def extract_date(self, day, time):
        day = self.condition_day(day)
        (hours, minutes) = self.condition_time(time)
        return spanish_date_conditioner(self.filename, day, hours, minutes)

    def condition_day(self, day_string):
        re_date = re.compile('\d{1,2}')
        indices = [d.start() for d in re_date.finditer(day_string)]
        day = day_string[indices[0]:].rstrip(' ')
        day = int(day)
        return day

    def condition_time(self, time_string):
        time_string = time_string[0:5]
        (hours, minutes) = time_string.split('.')
        hours = int(hours)
        minutes = int(minutes)
        return [hours, minutes]
