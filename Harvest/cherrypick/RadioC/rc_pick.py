import pdb
import os, sys

mypath = os.path.join(os.path.dirname(__file__))
sys.path.extend([os.path.join(mypath,'..'), os.path.join(mypath, '..', 'BBC3')])
import re

import common.wikid.wikidata as wd
import common.objects as obj
from common.utilities.path import root_path
from common.utilities.pdf_file import PDFFile
from common.utilities.string import string_similarity
from cherrypick.pdf_source_base import PdfSourceBase
from pathlib import Path
import rc_parser as rcp
from common.utilities.date import spanish_date_conditioner
from download.single_day import SingleDay

class EndOfHeaderNotFound(Exception):
    pass

class MalformedComposerString(ValueError):
    pass

class RCPick(PdfSourceBase):

    __PROVIDER__ = 'RadioC'
    __DEFAULT_RC_REPO_PATH__ = os.path.join(os.path.dirname(__file__), *['..']*3, 'Repo', __PROVIDER__)

    @classmethod
    def manage(cls, repo_dir = __DEFAULT_RC_REPO_PATH__):
        return super(cls, cls).manage(repo_dir)

    def extract_text_from_pdf(self):
        text = ""
        for t in self.pdf.readpage():
            text += t
        return text

    __RC_COMPOSER_LINE_RE__ = u'([A-ZÀ-Ý][A-ZÀ-Ý\.,\s\/\-]{2,}:)'
    @staticmethod
    def separate_composers(cstring):
        result = []
        re_comp = re.compile(RCPick.__RC_COMPOSER_LINE_RE__, re.UNICODE)
        temp  = re_comp.split(cstring)
        temp = [r for r in temp if len(r) > 0]
        #
        # get rid of all the cruft before a composer name
        #
        while len(temp) > 0:
            if re_comp.match(temp[0]):
                break
            else:
                temp.remove(temp[0])
        tmpsz = len(temp)
        if tmpsz == 0:                            # line does not have composers
            return result
        if (tmpsz % 2) != 0:
            raise MalformedComposerString(cstring)
        idx = 0
        while (idx < len(temp)):
            result.append(''.join(temp[idx:idx+2]))
            idx += 2

        for w in result:
            yield w

    def extract_composer(self):
        lexer  = rcp.RCLexer()
        parser = rcp.RCParser()
        for cl, date, time in self.find_composer_lines():
            for work in RCPick.separate_composers(cl):
                rec = None
                try:
                    rec = parser.safe_parse(lexer.tokenize(work))
                except (rcp.RCParserError, rcp.rc_lex.LexicalError, MalformedComposerString) as rcpe:
                    print("Parse error: %s" % (rcpe), file=sys.stderr)
                if rec:
                    yield rec, date, time
        self.pdf.close()

    def parse(self):
        for rec, date, time in self.extract_composer():
            save_composer = None
            if type(rec.composer) != obj.Composer:
                save_composer = rec.composer
                fc = SingleDay.find_first_composer(rec.composer)
                rec.composer = self.retrieve_composer(fc)
            rec.performance = obj.Performance(self.extract_date(date, time), RCPick.__PROVIDER__)
            yield rec

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
        result = None
        day = self.condition_day(day)
        (hours, minutes) = self.condition_time(time)
        try:
            result = spanish_date_conditioner(self.filename, day, hours, minutes)
        except ValueError as e:
            #
            # we need to cater for blatantly wrong dates. Grrr....
            #
            print("%s: file:%s day:%d hours:%d minutes:%d" % (str(e), self.filename, day, hours, minutes), file=sys.stderr)
            day = 1
            result = spanish_date_conditioner(self.filename, day, hours, minutes)
        return result

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
