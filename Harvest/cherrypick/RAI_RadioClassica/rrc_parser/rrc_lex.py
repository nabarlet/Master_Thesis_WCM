#
# This code perform the lexical analysis of the text of
# the programs issued by RAI - Radio3 Classica
#
import pdb
import sys,os
import re
from sly import Lexer

sys.path.append(os.path.join(os.path.dirname(__file__)))

from section_base import RRCLexerBase

class LexicalError(NameError):
    pass
#
# the actual lexer object
#

class RRCLexer(Lexer, RRCLexerBase):
    """
        RCCLexer():

        is a lexical analyzer derived from the sly.Lexer object
        needed to grok the lexical vocabulary of RRC files
    """

    literals = { COLON, SEMI, DOT, COMMA, EOL, }
    tokens = \
    {
            COLON,
            SEMI,
            DOT,
            COMMA,
            EOL,
            DURATA,
            DUR_VALUE,
            TIME_SECTION,
            YEAR,
            SINGLE_DASH,
            LONG_DASH,
            DIRETTO_DA,
            OP_NUM,
            NUMBER,
            WORD,
            E_CONJ,
    }
    ignore = ' \t'
    #
    # Lexical definitions for lex
    #
    COLON = ':'
    SEMI  = ';'
    DOT   = '\.'
    COMMA = ','
    EOL  = r'\s*\n+'
    DURATA = r'[Dd][Uu][Rr][Aa][Tt][Aa]:?'
    DUR_VALUE = r'\d?[Hh]?\d?\d\.\d\d'
    TIME_SECTION = r'\d\d:\d\d\s+[\-–]\s+\d\d:\d\d'
    YEAR = r'\d{4}'
    DIRETTO_DA = r'[Dd]irett[oa]\s+da'
    OP_NUM = r'[Oo][Pp]\.\s*\d+[A-Za-z]*'
    NUMBER = r'\d+'
    WORD = u'[\w"”“\'’‘\`\!\?\-–—\&/\\\#\(\)\[\]\{\}…|°]+'
    WORD['e'] = E_CONJ
    WORD['-'] = SINGLE_DASH
    WORD['–'] = LONG_DASH
    
    last_eol_column = 0

    @_(EOL)
    def EOL(self, t):
        only_newlines = re.sub('[ \t]+', '', t.value)
        self.lineno += len(only_newlines)
        RRCLexer.last_eol_column = self.index
        return t

    def error(self, t):
        """
           error(token)

           will not raise an exception here because it's practically
           impossible to catch the exception in the token generator without
           loosing the whole state. So we simply gobble the culprit, signal it
           and go on.
        """
        self.error_handling(t)
