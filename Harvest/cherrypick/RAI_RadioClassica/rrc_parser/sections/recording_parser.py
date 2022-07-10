#
# This code perform the lexical analysis of the text of
# the programs issued by RAI - Radio3 Classica
#
# recording section
#
import pdb
import sys, os
import re
from sly import Lexer, Parser

from rrc_parser.section_base import RRCLexerBase, RRCParserBase

#
# the actual lexer object
#

class RRCRecordingLexer(Lexer, RRCLexerBase):
    """
        RCCRecordingLexer():

        is a lexical analyzer derived from the sly.Lexer object
        needed to grok the lexical vocabulary of RRC file recording records
    """

    literals = { EOL, }
    tokens   = { EOL, DURATA, DURATA_VALUE, NUMBER, WORD, }
    ignore   = ' \t'
    #
    # Lexical definitions for lex
    #
    EOL  = r'\s*\n+'
    DURATA = r'[Dd]urata[:]?'
    DURATA_VALUE = r'(\d+h\d{2}\.\d{2}|\d{1,2}\.\d{2})'
    NUMBER = r'\d+'
    WORD = r'[:,;\w"”“\'’‘\`\!\?\-–—\&/\\\#\(\)\[\]\{\}…\|\.]+'
    
    @_(EOL)
    def EOL(self, t):
        return self.eol_handling(t)

    def error(self, t):
        return self.error_handling(t)

from common.utilities.string import join
import common.objects as obj

class RRCRecordingParser(Parser, RRCParserBase):
    debugfile = os.path.join(os.path.dirname(__file__), '..', '..', 'test', 'parser_debug.out')
    tokens = RRCRecordingLexer.tokens
    start = 'recording_section'

    @_('recording')
    def recording_section(self, p):
        return p.recording

    @_('composer title_and_other_info durata label')
    def recording(self, p):
        composer = obj.Composer(p.composer)
        other_info = title = None
        title = p.title_and_other_info[0].rstrip()
        other_info = [s.rstrip() for s in p.title_and_other_info[1:]]
        result = obj.Recording(composer, other_info, title, dur = p.durata, label = p.label)
        return result
    
    @_('one_line_string EOL')
    def composer(self, p):
        return p.one_line_string
    
    @_('multiple_line_string')
    def title_and_other_info(self, p):
        return p.multiple_line_string

    @_('DURATA DURATA_VALUE EOL')
    def durata(self, p):
        result = obj.Duration(p.DURATA_VALUE)
        return result

    @_('one_line_string EOL')
    def label(self, p):
        return p.one_line_string

    #
    # multi line string
    #
    @_('one_line_string EOL')
    def multiple_line_string(self, p):
        mls = []
        mls.append(p.one_line_string)
        return mls

    @_('multiple_line_string one_line_string EOL')
    def multiple_line_string(self, p):
        p.multiple_line_string.append(p.one_line_string)
        return p.multiple_line_string
    #
    # rule for multiple WORDs (name) on a single string
    #
    @_('one_line_string word')
    def one_line_string(self, p):
        return p.one_line_string + ' ' + p.word

    @_('word')
    def one_line_string(self, p):
        return p.word

    @_('WORD')
    def word(self, p):
        return self.name_WORD_rule(p)

    @_('NUMBER')
    def word(self, p):
        return p.NUMBER

    def error(self, p):
        return self.error_handling(p)
