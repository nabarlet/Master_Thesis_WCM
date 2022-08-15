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
            NUMBER,
            WORD,
            LPAR,
            RPAR,
            SINGLE_QUOTE,
            DOUBLE_QUOTE,
    }
    #
    # Lexical definitions for lex
    #
    DOT   = r'\.'
    LPAR  = r'\('
    RPAR  = r'\)'
    SINGLE_QUOTE = r"'"
    DOUBLE_QUOTE = r'"'
    # DUR_TYPE_1 = r'\(\d+\.\d{2}\)'
    # DUR_TYPE_2 = r"\(\d+'\d+\"\)"
    # DUR_TYPE_3 = r"\(\d+\)"
    NUMBER = r'\d+'
    COMPOSER = r'[A-ZÀ-Ú\s\/\.\-”,„]+:'
    WORD = r'[\w\s,:;\/\'“"´”"̈\[\]-–-*¡„]+'
    
    last_eol_column = 0

    def error(self, t):
        column = t.index - RCLexer.last_eol_column
        raise LexicalError("lexical error: illegal character \"%s\" in line %d column %d" % (t.value[0], self.lineno, column))
