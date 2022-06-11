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
    literals = { COLON, DOT, COMMA, }
    tokens = \
    {
            COLON,
            SEMI,
            DOT,
            COMMA,
            DURATION,
            COMPOSER,
            CONDUCTOR_TAG,
            WORD,
    }
    #
    # Lexical definitions for lex
    #
    COLON = ':'
    SEMI  = ';'
    DOT   = r'\.'
    COMMA = ','
    DURATION = r'\(\d{1,2}\.\d{2}\)'
    COMPOSER = r'[A-Z\s\/\.]+:'
    CONDUCTOR_TAG = r'Dir.?:\s+'
    WORD = r'.+'
    
    last_eol_column = 0

    def error(self, t):
        column = t.index - RCLexer.last_eol_column
        raise LexicalError("lexical error: illegal character \"%s\" in line %d column %d" % (t.value[0], self.lineno, column))
