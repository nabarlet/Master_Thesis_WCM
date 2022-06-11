import pdb
import os, sys

from utilities.path import root_path
from utilities.date import date_conditioner
from utilities.string import join
from sly import Parser
from rc_parser.rc_lex import RCLexer
import objects as obj

class ParserError(NameError):
    pass

class RCParser(Parser):
    debugfile = os.path.join(root_path, 'test', 'parser_debug.out')
    tokens = RCLexer.tokens
    precedence = (
        ('left', COMMA),
        ('right', ORCH_COMMA),
    )

    #
    # THIS IS YET TBD
    #

    def error(self, p):
        """
            +error()+: attempts to resynchronize at EOL
        """
        tok = p
        if p:
            column = p.index - RCLexer.last_eol_column
            print("parser error: unexpected token %s (\"%s\") at line %d column %d" % (p.type, p.value, p.lineno, column), file=sys.stderr)
            while True:
                tok = next(self.tokens, None)
                if not tok or tok.type == 'EOL':
                    break
            self.errok()
        else:
            raise ParserError("Unexpected EOF")
        return tok
