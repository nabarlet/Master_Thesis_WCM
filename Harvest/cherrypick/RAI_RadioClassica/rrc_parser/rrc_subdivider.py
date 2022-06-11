import pdb
import re, sys
sys.path.append('..')

from rrc_parser.section_base import RRCLexicalError, RRCParserError
from common.utilities.string import join

class RRCSubdividerError(RRCParserError):
    pass

class RRCSubdividerEmpty(RRCParserError): # empty-line bypass
    pass

class SectionMeta:
    def __init__(self, type, re_match, lexer = None, parser = None):
        self.type = type
        self.re_match = re_match
        self.lexer = lexer
        self.parser = parser
        self.__match__ = re.compile(self.re_match)

    def inspect(self, lineno, sectno):
        result = "==== Section %s (line: %d, section number: %d) ===\n" % (self.type, lineno, sectno)
        return result

    def match(self, text):
        return self.__match__.findall(text)

class Section(SectionMeta):
    def __init__(self, type, re_match, lineno, sectno, lexer = None, parser = None):
        super().__init__(type, re_match, lexer = lexer, parser = parser)
        self.lines = None
        self.lineno = lineno
        self.sectno = sectno

    def inspect(self):
        result = super().inspect(self.lineno, self.sectno)
        result += ''.join(self.lines)
        return result

    def parse(self):
        result = None
        if self.lexer and self.parser:
            lexer = self.lexer()
            lexer.lineno = self.lineno
            lexer.sectno = self.sectno
            parser = self.parser()
            parser.sectno = self.sectno
            coalesced_text = join(self.lines, '')
            coalesced_text += '\n'
            tokens = lexer.tokenize(coalesced_text)
            result = parser.parse(tokens)
        return result

import rrc_parser.sections as rps

class RRCSubdivider:

    SECTION_TYPES = {
        'header':    SectionMeta('header', '\A\s*\d{1,2}\s+\w+\s+\d{4}\s*\Z', lexer = rps.RRCHeaderLexer, parser = rps.RRCHeaderParser),
        'anniversaries': SectionMeta('anniversaries', '\d{4}\s+[-–]\s*\d{1,2}', lexer = rps.RRCAnniversariesLexer, parser = rps.RRCAnniversariesParser),
        'recording': SectionMeta('recording', '(?i)durata', lexer = rps.RRCRecordingLexer, parser = rps.RRCRecordingParser),
        'program':   SectionMeta('program', '\d{2}:\d{2}\s*[-–]\s+\d{2}:\d{2}', lexer = rps.RRCProgramLexer, parser = rps.RRCProgramParser),
        'concert':   SectionMeta('concert', '([Cc]oncerto\s+d|\d{1,2}\s+\w+\s*[\-–]?\s+\d{4}|[\-–]\s*\d{1,2}\/\d{2}\/\d{4}|[Oo]rchestra\s+[Ss]infonica\s+[Nn]azionale\s+della\s+[Rr][Aa][Ii])'),
        'cdrecord':  SectionMeta('cdrecord', '[.\n]+'), # basically everything else can only be a cd record
    }
    SECTION_SEQUENCE = {
        'start':  [ 'header' ],
        'header': [ 'anniversaries', 'program' ],
        'anniversaries': [ 'program' ],
        'program': [ 'recording', 'concert', 'cdrecord' ],
        'recording': [ 'recording', 'program', 'header' ],
        'cdrecord': ['recording'],
        'concert': ['recording'],
    }

    EMPTY_LINE = re.compile('\A\s*\n+')

    def __init__(self, text_file_in_lines):
        self.text_file = text_file_in_lines
        self.sections = []
        self.ignored_sections = []
        self.last_section = 'start'

    def create_sections(self):
        accu_lines = []
        lineno = 0
        sectno = 0
        for l in self.text_file:
            if RRCSubdivider.EMPTY_LINE.match(l):
                try:
                    new_sect = self.lookup_section(accu_lines, lineno, sectno)
                    new_sect.lines = accu_lines
                    self.sections.append(new_sect)
                except RRCSubdividerError as msg:
                    self.ignored_sections.append(str(msg) + ". Ignored")
                except RRCSubdividerEmpty: # bypass
                    pass
                finally:
                    accu_lines = []
                    sectno += 1
            else:
                accu_lines.append(l)
            lineno += 1

    def lookup_section(self, lines, lineno, sectno):
        result = None
        coalesced = join(lines, '')
        if coalesced == '': # skip empty lines
            raise RRCSubdividerEmpty
        for skey in RRCSubdivider.SECTION_SEQUENCE[self.last_section]:
            sm = RRCSubdivider.SECTION_TYPES[skey]
            m = sm.match(coalesced)
            if len(m) > 0:  
                result = Section(sm.type, sm.re_match, lineno, sectno, lexer = sm.lexer, parser = sm.parser)
                self.last_section = skey
                break
        if not result:
            raise RRCSubdividerError("=== section %d:%d type not found for text\n%s" % (sectno, lineno, coalesced.strip()))
        return result

    def inspect(self):
        for s in self.sections:
            yield s.inspect()

    def parse(self):
        result = []
        self.create_sections()
        for s in self.sections:
            try:
                parsed = s.parse()
                if parsed:
                    if type(parsed) is list:
                        for p in parsed:
                            yield p
                    else:
                        yield parsed
            except (RRCLexicalError, RRCParserError):
                continue
