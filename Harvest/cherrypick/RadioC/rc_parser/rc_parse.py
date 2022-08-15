import pdb
import os, sys

from common.utilities.path import root_path
from common.utilities.string import join, __UNK__
from sly import Parser
from rc_parser.rc_lex import RCLexer
import common.objects as obj

class RCParserError(NameError):
    pass

class RCParser(Parser):
    debugfile = os.path.join(root_path, 'cherrypick', 'RadioC', 'test', 'parser_debug.out')
    tokens = RCLexer.tokens
    start = 'data_line'

    @_('COMPOSER title duration DOT musicians DOT')
    def data_line(self, p):
        comp = p.COMPOSER.rstrip(':')
        rec = obj.Recording(comp = comp, title = p.title, oi = p.musicians, dur = p.duration)
        return rec

    @_('COMPOSER title duration DOT musicians')
    def data_line(self, p):
        comp = p.COMPOSER.rstrip(':')
        rec = obj.Recording(comp = comp, title = p.title, oi = p.musicians, dur = p.duration)
        return rec

    @_('COMPOSER title DOT')
    def data_line(self, p):
        comp = p.COMPOSER.rstrip(':')
        rec = obj.Recording(comp = comp, title = p.title, oi = __UNK__, dur = obj.Duration.create(__UNK__))
        return rec

    @_('COMPOSER title duration musicians')
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

    @_('title DOT')
    def title(self, p):
        return p.title + p.DOT

    @_('title LPAR')
    def title(self, p):
        return p.title + p.LPAR

    @_('title RPAR')
    def title(self, p):
        return p.title + p.RPAR

    @_('title NUMBER')
    def title(self, p):
        return p.title + ' ' + p.NUMBER

    @_('LPAR NUMBER DOT NUMBER RPAR')
    def duration(self, p):
        value = p.NUMBER0 + p.DOT + p.NUMBER1
        return obj.Duration.create(value, parser=obj.Duration.dot_parser)

    @_('LPAR NUMBER SINGLE_QUOTE NUMBER DOUBLE_QUOTE RPAR')
    def duration(self, p):
        value = p.NUMBER0 + p.SINGLE_QUOTE + p.NUMBER1 + p.DOUBLE_QUOTE
        return obj.Duration.create(value, parser=obj.Duration.quote_parser)

    @_('LPAR NUMBER RPAR')
    def duration(self, p):
        value = p.NUMBER
        return obj.Duration.create(value, parser=obj.Duration.single_number_parser)

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

    @_('musicians LPAR')
    def musicians(self, p):
        return p.musicians + ' ' + p.LPAR

    @_('musicians RPAR')
    def musicians(self, p):
        return p.musicians + p.RPAR

    @_('musicians DOT')
    def musicians(self, p):
        return p.musicians + p.DOT

    def error(self, tok):
        raise RCParserError(tok)

    @staticmethod
    def remove_parenthesis(string):
        return string[1:-1]
