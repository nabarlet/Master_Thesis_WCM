import pdb
import os, sys

from utilities.path import root_path
from utilities.string import join
from sly import Parser
from rc_parser.rc_lex import RCLexer
import objects as obj

class RCParserError(NameError):
    pass

class RCParser(Parser):
    debugfile = os.path.join(root_path, 'cherrypick', 'RadioC', 'test', 'parser_debug.out')
    tokens = RCLexer.tokens
    start = 'data_line'

    @_('COMPOSER title LPAR duration RPAR DOT musicians')
    def data_line(self, p):
        comp = p.COMPOSER.rstrip(':')
        rec = obj.Recording(comp = comp, title = p.title, oi = p.musicians, dur = p.duration)
        return rec

    @_('WORD')
    def title(self, p):
        return p.WORD

    @_('title WORD')
    def title(self, p):
        return p.title + ' ' + p.WORD

    @_('NUMBER DOT NUMBER')
    def duration(self, p):
        return p.NUMBER0 + p.DOT + p.NUMBER1

    @_('NUMBER')
    def duration(self, p):
        return p.NUMBER

    @_('')
    def musicians(self, p):
        """
            empty musicians rule
        """
        return ''

    @_('WORD')
    def musicians(self, p):
        return p.WORD

    @_('musicians WORD')
    def musicians(self, p):
        return p.musicians + ' ' + p.WORD

    def error(self, tok):
        raise RCParserError(tok)
