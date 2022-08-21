#
# This code perform the lexical analysis of the text of
# the programs issued by Radio C (Spain)
#
import pdb
import sys
import re
from sly import Lexer

class LexicalError(NameError):
    pass
#
# the actual lexer object
#

class RCLexer(Lexer):
    """
        RCLexer():

        is a lexical analyzer derived from the sly.Lexer object
        needed to grok the lexical vocabulary of RC files
    """

    ignore = ' \t'
    literals = { DOT, LPAR, RPAR, SINGLE_QUOTE, DOUBLE_QUOTE }
    tokens = \
    {
            DOT,
            COMPOSER,
            YEAR,
            NUMBER,
            WORD,
            LPAR,
            RPAR,
            SINGLE_QUOTE,
            DOUBLE_QUOTE,
            # ORD_NUMBER,
    }
    #
    # Lexical definitions for lex
    #
    DOT   = r'\.'
    LPAR  = r'\('
    RPAR  = r'\)'
    SINGLE_QUOTE = r"['‟’‘]"
    DOUBLE_QUOTE = r'["”]'
    YEAR   = r'\s*[12]\d{3}\s*'
    NUMBER = r'\d+'
    COMPOSER = r'[A-ZÀ-Ú\s\/\.\-‘”,„]+:'
    #WORD = r'([\w\s,:;\/\'“"´’"̈\[\]-–-*¡„\+\*&\?!…#►—−=]+|(^([Oo][Pp]|[Nn]|[Mm][Oo][Vv]|[Kk]|[Dd])[\.|º]\s+\d+))'
    WORD = r'[\w\s,:;\/\'“"´’"̈\[\]-–-*¡„\+\*&\?!…#►—−=]+'
    # ORD_NUMBER = r'([Oo][Pp]|[Nn]|[Mm][Oo][Vv]|[Kk]|[Dd])\s*[\.|º]\s*\d+'
    
    last_eol_column = 0

    def error(self, t):
        column = t.index - RCLexer.last_eol_column
        raise LexicalError("lexical error: illegal character \"%s\" in line %d column %d" % (t.value[0], self.lineno, column))
