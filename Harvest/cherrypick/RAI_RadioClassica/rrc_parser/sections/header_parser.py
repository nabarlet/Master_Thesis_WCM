#
# This code perform the lexical analysis of the text of
# the programs issued by RAI - Radio3 Classica
#
import pdb
import sys,os
import re

sys.path.append(os.path.join('..', '..', '..'))

from sly import Lexer, Parser
from rrc_parser.section_base import RRCLexerBase, RRCParserBase

#
# the actual lexer object
#

class RRCHeaderLexer(Lexer, RRCLexerBase):
    """
        RCCHeaderLexer():

        is a lexical analyzer derived from the sly.Lexer object
        needed to grok the lexical vocabulary of RRC file headers
    """

    literals = { EOL }
    tokens = { EOL, DATE_TOKEN }
    ignore = ' \t'
    #
    # Lexical definitions for lex
    #
    EOL  = r'\s*\n+'
    DATE_TOKEN = r'\d{1,2}\s+\w+\s+\d{4}'
    
    @_(EOL)
    def EOL(self, t):
        return self.eol_handling(t)

    def error(self, t):
        return self.error_handling(t)

from common.utilities.date import italian_date_conditioner
import common.objects as obj

class RRCHeaderParser(Parser, RRCParserBase):
    tokens = RRCHeaderLexer.tokens

    @_('file_date')
    def file(self, p):
        result = obj.File()
        result.set_date(p.file_date)
        return result

    @_('date EOL')
    def file_date(self, p):
        return p.date
    #
    # date format
    #
    @_('DATE_TOKEN')
    def date(self, d):
        (day, month, year) = d.DATE_TOKEN.split()
        datestring = italian_date_conditioner(day, month, year)
        return datestring

    def error(self, p):
        return self.error_handling(p)
