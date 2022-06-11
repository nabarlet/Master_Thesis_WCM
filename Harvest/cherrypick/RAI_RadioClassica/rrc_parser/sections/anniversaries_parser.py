#
# This code perform the lexical analysis of the text of
# the programs issued by RAI - Radio3 Classica
#
import pdb
import sys
import re
from sly import Lexer, Parser

from rrc_parser.section_base import RRCLexerBase, RRCParserBase

#
# the actual lexer object
#

class RRCAnniversariesLexer(Lexer, RRCLexerBase):
    """
        RCCAnniversariesLexer():

        is a lexical analyzer derived from the sly.Lexer object
        needed to grok the lexical vocabulary of RRC file anniversaries
        section
    """

    literals = { EOL }
    tokens   = { EOL, YEAR, DAY, SINGLE_DASH, WORD }
    ignore   = ' \t'
    #
    # Lexical definitions for lex
    #
    EOL  = r'\s*\n+'
    YEAR = r'[12]?\d{3}'
    DAY = r'[1-3]?[0-9]'
    SINGLE_DASH = r'[\-–—]'
    WORD = r'[^\s\d]+' # anything that is not a space nor a number
    
    @_(EOL)
    def EOL(self, t):
        return self.eol_handling(t)

    def error(self, t):
        return self.error_handling(t)

from common.utilities.string import join
import common.objects as obj

class RRCAnniversariesParser(Parser, RRCParserBase):
    tokens = RRCAnniversariesLexer.tokens
    start = 'anniversaries_section'

    @_('anniversaries')
    def anniversaries_section(self, p):
        return p.anniversaries

    @_('anniversary')
    def anniversaries(self, p):
        anniversaries = []
        anniversaries.append(p.anniversary)
        return anniversaries

    @_('anniversaries anniversary')
    def anniversaries(self, p):
        p.anniversaries.append(p.anniversary)
        return p.anniversaries

    #
    # anniversary
    #
    @_('name date SINGLE_DASH date EOL')
    def anniversary(self, p):
        ann = obj.Anniversary(p.name, p.date0, p.date1)
        return ann

    @_('name date EOL')
    def anniversary(self, p):
        ann = obj.Anniversary(p.name, p.date)
        return ann

    #
    # rule for multiple WORDs (name)
    #
    @_('name WORD')
    def name(self, p):
        return self.name_name_rule(p)

    @_('WORD')
    def name(self, p):
        return self.name_WORD_rule(p)

    @_('DAY WORD YEAR')
    def date(self, d):
        return self.date_rule(d.DAY, d.WORD, d.YEAR)

    @_('YEAR')
    def date(self, d):
        return self.date_rule(None, None, d.YEAR)

    def error(self, p):
        return self.error_handling(p)
