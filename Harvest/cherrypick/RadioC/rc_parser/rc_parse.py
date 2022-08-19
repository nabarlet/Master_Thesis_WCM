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

    def safe_parse(self, tokens):
        result = self.parse(tokens)
        if not result:
            result = self.read_final_result()
        return result

    __FINAL_RESULT__ = None
    def read_final_result(self):
        """
            read_final_result():

            this is a brutal hack trying to save the intermediate result when
            the parser encounters an error.
        """
        result = RCParser.__FINAL_RESULT__
        RCParser.__FINAL_RESULT__ = None
        return result

    @_('COMPOSER other_info')
    def data_line(self, p):
        # pdb.set_trace()
        comp = p.COMPOSER.rstrip(':')
        result = p.other_info
        result.composer = comp
        RCParser.__FINAL_RESULT__ = result
        return result

    @_('title duration DOT musicians', 'title duration musicians', 'title duration DOT musicians error', 'title duration musicians error')
    def other_info(self, p):
        # pdb.set_trace()
        result = obj.Record(comp = None, title = p.title, oi = p.musicians, dur = p.duration)
        return result

#   @_('other_info DOT other_info')
#   def other_info(self, p):
#       # pdb.set_trace()
#       p.other_info0 += (' ' + p.other_info1)
#       return p.other_info0

    @_('word_element')
    def title(self, p):
        # pdb.set_trace()
        return p.word_element

    @_('title word_element')
    def title(self, p):
        # pdb.set_trace()
        return p.title + ' ' + p.word_element

    @_('title ponctuation')
    def title(self, p):
        # pdb.set_trace()
        return p.title + p.ponctuation

    @_('LPAR NUMBER DOT NUMBER RPAR')
    def duration(self, p):
        # pdb.set_trace()
        value = p.NUMBER0 + p.DOT + p.NUMBER1
        return obj.Duration.create(value, parser=obj.Duration.dot_parser)

    @_('LPAR NUMBER SINGLE_QUOTE NUMBER DOUBLE_QUOTE RPAR')
    def duration(self, p):
        # pdb.set_trace()
        value = p.NUMBER0 + p.SINGLE_QUOTE + p.NUMBER1 + p.DOUBLE_QUOTE
        return obj.Duration.create(value, parser=obj.Duration.quote_parser, attrs={ 'dsep': RCLexer.DOUBLE_QUOTE, 'ssep': RCLexer.SINGLE_QUOTE, })

    @_('LPAR NUMBER RPAR')
    def duration(self, p):
        # pdb.set_trace()
        value = p.NUMBER
        return obj.Duration.create(value, parser=obj.Duration.single_number_parser)

    @_('')
    def musicians(self, p):
        """
            empty musicians rule
        """
        # pdb.set_trace()
        return ''

    @_('word_element')
    def musicians(self, p):
        # pdb.set_trace()
        return p.word_element

    @_('musicians word_element')
    def musicians(self, p):
        # pdb.set_trace()
        return p.musicians + ' ' + p.word_element

    @_('musicians ponctuation')
    def musicians(self, p):
        # pdb.set_trace()
        return p.musicians + p.ponctuation

    @_('WORD')
    def word_element(self, p):
        # pdb.set_trace()
        return p.WORD

    @_('LPAR')
    def word_element(self, p): # open parenthesis needs a space before it
        # pdb.set_trace()
        return p.LPAR

    @_('NUMBER')
    def word_element(self, p):
        # pdb.set_trace()
        return p.NUMBER

    @_('year')
    def word_element(self, p):
        # pdb.set_trace()
        return p.year

    @_('DOT')
    def ponctuation(self, p):
        # pdb.set_trace()
        return p.DOT

    @_('RPAR')
    def ponctuation(self, p):
        # pdb.set_trace()
        return p.RPAR

    @_('SINGLE_QUOTE')
    def ponctuation(self, p):
        # pdb.set_trace()
        return p.SINGLE_QUOTE

    @_('DOUBLE_QUOTE')
    def ponctuation(self, p):
        # pdb.set_trace()
        return p.DOUBLE_QUOTE

    @_('LPAR NUMBER RPAR')
    def year(self, p):
        # pdb.set_trace()
        return p.LPAR + p.NUMBER + p.RPAR

    def error(self, tok):
        #
        # error (almost) quietly gets to the end trying to save what's savable
        #
        error_message = "Syntax Error: discarded \"%s\" "
        tok_discarded = ''
        while tok:
            value = tok.value
            if tok.type == 'error':
                value = tok.value.value
            tok_discarded += value
            tok = next(self.tokens, None)
        if len(tok_discarded) > 10:
            print(error_message % (tok_discarded), file=sys.stderr)
        self.errok()
        return tok
