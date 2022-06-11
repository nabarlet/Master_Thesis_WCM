#
# This code perform the lexical analysis of the text of
# the programs issued by RAI - Radio3 Classica
#
import pdb
import os, sys
import re

class RRCLexicalError(NameError):
    pass
#
# the actual lexer object
#

class RRCLexerBase:
    """
        RRCLexerBase:

        is the base of all lexical analyzers and acts as a mixin object
    """

    last_eol_column = 0

    def __init__(self):
        self.sectno = 0

    def error_handling(self, t):
        """
           error(token)

           will not raise an exception here because it's practically
           impossible to catch the exception in the token generator without
           loosing the whole state. So we simply gobble the culprit, signal it
           and go on.
        """
        column = t.index - RRCLexerBase.last_eol_column
        raise RRCLexicalError("RRCLexerBase lexical error: illegal character \"%s\" in section %d line %d column %d" % (t.value[0], self.sectno, self.lineno, column))

    def eol_handling(self, t):
        only_newlines = re.sub('[ \t]+', '', t.value)
        self.lineno += len(only_newlines)
        RRCLexerBase.last_eol_column = self.index
        return t

from common.utilities.path import root_path
from common.utilities.date import italian_date_conditioner
from common.utilities.string import join
import common.objects as obj

class RRCParserError(NameError):
    pass

class RRCParserBase:
    debugfile = os.path.join(root_path, 'test', 'parser_debug.out')

    def __init__(self):
        self.sectno = 0

    #
    # to be used with @_('name WORD')
    #
    def name_name_rule(self, p):
        return p.name + ' ' + p.WORD

    #
    # to be used with @_('WORD')
    #
    def name_WORD_rule(self, p):
        return p.WORD

    #
    # date format rule
    #
    # to be used with @_('NUMBER WORD YEAR')
    #
    def date_rule(self, dd, mm, yyyy):
        datestring = italian_date_conditioner(dd, mm, yyyy)
        return datestring


    def empty_rule(self, p):
        return p

    def error_handling(self, p):
        """
            +error()+: attempts to resynchronize at EOL
        """
        tok = p
        if p:
            column = p.index - RRCLexerBase.last_eol_column
            print("RRCParser error: unexpected token %s (\"%s\") in section %d at line %d column %d - attempting to resynchronize." % (p.type, p.value, self.sectno, p.lineno, column), file=sys.stderr, end='')
            while True:
                tok = next(self.tokens, None)
                print('.', end='', file=sys.stderr)
                if not tok or tok.type == 'EOL':
                    break
            print(" succeded!", file=sys.stderr)
            self.errok()
        else:
            raise RRCParserError("RRCParser error: uuuuh ugly! Unexpected EOF! Trying to continue anyway...")
        return tok
