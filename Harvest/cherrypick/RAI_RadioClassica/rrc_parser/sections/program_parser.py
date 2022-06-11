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

class RRCProgramLexer(Lexer, RRCLexerBase):
    """
        RCCHeaderLexer():

        is a lexical analyzer derived from the sly.Lexer object
        needed to grok the lexical vocabulary of RRC file headers
    """

    literals = { EOL }
    tokens   = { EOL, TIME_SECTION, WORD }
    ignore   = ' \t'
    #
    # Lexical definitions for lex
    #
    EOL  = r'\s*\n+'
    TIME_SECTION = r'\d\d:\d\d\s+[\-–]\s+\d\d:\d\d'
    WORD = r'[:,\w"”“\'’‘\`\!\?\-–—\&/\\\#\(\)\[\]\{\}…]+'
    
    @_(EOL)
    def EOL(self, t):
        return self.eol_handling(t)

    def error(self, t):
        return self.error_handling(t)

from common.utilities.string import join
import common.objects as obj

class RRCProgramParser(Parser, RRCParserBase):
    tokens = RRCProgramLexer.tokens
    start = 'program_section'

    @_('program_title')
    def program_section(self, p):
        return p.program_title

    @_('name TIME_SECTION EOL', 'TIME_SECTION name EOL', 'name EOL TIME_SECTION EOL')
    def program_title(self, p):
        p_title = obj.TimeSection(join(p.name), p.TIME_SECTION)
        return p_title
    
    @_('TIME_SECTION EOL')
    def program_title(self, p):
        name = None
        p_title = obj.TimeSection(name, p.TIME_SECTION)
        return p_title
    
    #
    # rule for multiple WORDs (name)
    #
    @_('name WORD')
    def name(self, p):
        return p.name + ' ' + p.WORD

    @_('WORD')
    def name(self, p):
        return p.WORD

    def error(self, p):
        return self.error_handling(p)
