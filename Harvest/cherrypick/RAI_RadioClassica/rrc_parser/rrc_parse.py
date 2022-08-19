import pdb
import os, sys

from utilities.path import root_path
from utilities.date import italian_date_conditioner
from utilities.string import join
from sly import Parser
from rrc_parser.rrc_lex import RRCLexer
import objects as obj

class ParserError(NameError):
    pass

class RRCParser(Parser):
    debugfile = os.path.join(root_path, 'test', 'parser_debug.out')
    tokens = RRCLexer.tokens
    precedence = (
        ('left', COMMA),
        ('right', ORCH_COMMA),
    )

    def __init__(self):
        self.result = obj.File()

    @_('file_date anniversaries sections')
    def file(self, p):
        self.result.set_date(p.file_date)
        return p

    @_('date EOL')
    def file_date(self, p):
        return p.date
    #
    # date format
    #
    @_('NUMBER WORD YEAR')
    def date(self, d):
        datestring = italian_date_conditioner(d.NUMBER, d.WORD, d.YEAR)
        return datestring

    #
    # anniversaries
    #
    @_('empty') # can be empty
    def anniversaries(self, p):
        return p

    @_('anniversaries anniversary')
    def anniversaries(self, p):
        self.result.append_anniversary(p.anniversary)
        return p

    #
    # anniversary
    #
    @_('name date SINGLE_DASH date EOL')
    def anniversary(self, p):
        ann = obj.Anniversary(p)
        return ann

    @_('name date EOL')
    def anniversary(self, p):
        ann = obj.Anniversary(p)
        return ann

    #
    # sections
    #
    @_('section', 'sections section')
    def sections(self, p):
        self.result.append_time_section(p.section)
        return p

    @_('section_title recordings')
    def section(self, p):
        t_section = p.section_title
        t_section.recordings = p.recordings
        return t_section
    
    #
    # section title (four types)
    #
    @_('name TIME_SECTION EOL', 'TIME_SECTION name EOL', 'name EOL TIME_SECTION EOL', 'TIME_SECTION EOL')
    def section_title(self, p):
        s_title = obj.TimeSection(join(p.name), p.TIME_SECTION)
        return s_title

    @_('recording')
    def recordings(self, p):
        recs = [ p.recording ]
        return recs

    @_('recordings recording')
    def recordings(self, p):
        p.recordings.append(p.recording)
        return p.recordings

    @_('composer EOL phrase movements EOL performers EOL durata EOL label EOL')
    def recording(self, p):
        rec = obj.Record()
        rec.composer, rec.title, rec.performers, rec.duration, rec.label = p.composer, p.phrase, p.performers, p.durata, p.label
        return rec

    @_('name')
    def composer(self, p):
        return p.name

    #
    # movements: empty
    #          | movement
    #          | movements dash movement
    #          | movements dash movement EOL
    #
    @_('empty')
    def movements(self, p):
        return ''

    @_('movement')
    def movements(self, p):
        return p.movement

    @_('movements dash movement', 'movements dash movement EOL')
    def movements(self, p):
        return p.movements + p.dash + p.movement

    @_('phrase')
    def movement(self, p):
        return p.phrase
    #
    # performers: performer
    #           | performers SEMI performer
    #           | performers E_CONJ performer
    #
    @_('performer')
    def performers(self, p):
        if type(p.performer) is list: # orchestras + cond are lists
            result = p.performer
        else:
            result = [ p.performer ]
        return result

    @_('performers SEMI performer')
    def performers(self, p):
        p.performers.append(p.performer)
        return p.performers
    
    @_('performers E_CONJ performer')
    def performers(self, p):
        p.performers.append(p.performer)
        return p.performers

    #
    # performer: musician COMMA instrument
    #          | orchestra
    #          | orchestra DIRETTO_DA musician
    #          | orchestra COMMA performer
    #
    @_('musician COMMA instrument')
    def performer(self, p):
        perf = obj.Performer(p.musician)
        perf.role = p.instrument
        return perf

    @_('orchestra')
    def performer(self, p):
        orch = obj.Performer(p.orchestra)
        return orch

    @_('orchestra DIRETTO_DA musician')
    def performer(self, p):
        orch = obj.Performer(p.orchestra)
        cond = obj.Performer(p.musician)
        cond.role = "conductor"
        return [orch, cond]

    @_('orchestra COMMA performer %prec ORCH_COMMA')
    def performer(self, p):
        orch = obj.Performer(p.orchestra)
        cond = p.performer
        cond.role = "conductor"
        return [orch, cond]

    @_('name')
    def musician(self, p):
        return p.name

    @_('name')
    def instrument(self, p):
        return p.name

    @_('name')
    def orchestra(self, p):
        return p.name

    #
    # durata and label
    #

    @_('DURATA DUR_VALUE')
    def durata(self, p):
        return p.DUR_VALUE

    @_('phrase')
    def label(self, p):
        return p.phrase

    #
    # rule for multiple WORDs (name)
    #
    @_('name WORD')
    def name(self, p):
        return p.name + ' ' + p.WORD

    @_('WORD')
    def name(self, p):
        return p.WORD

    #
    # dashes
    #
    @_('SINGLE_DASH')
    def dash(self, p):
        return ' ' + p.SINGLE_DASH + ' '

    @_('LONG_DASH')
    def dash(self, p):
        return ' ' + p.LONG_DASH + ' '

    #
    # rule for complete phrases
    #
    @_('phrase_item')
    def phrase(self, p):
        return p.phrase_item

    @_('phrase phrase_item')
    def phrase(self, p):
        return p.phrase + p.phrase_item

    @_('name')
    def phrase_item(self, p):
        return p.name

    @_('NUMBER')
    def phrase_item(self, p):
        return ' ' + str(p.NUMBER) + ' '

    @_('SEMI')
    def phrase_item(self, p):
        return p.SEMI + ' '

    @_('COLON')
    def phrase_item(self, p):
        return p.COLON + ' '

    @_('DOT')
    def phrase_item(self, p):
        return p.DOT + ' '

    @_('dash')
    def phrase_item(self, p):
        return p.dash

    @_('E_CONJ')
    def phrase_item(self, p):
        return ' ' + p.E_CONJ + ' '

    @_('OP_NUM')
    def phrase_item(self, p):
        return ' ' + str(p.OP_NUM) + ' '

    @_('YEAR')
    def phrase_item(self, p):
        return str(p.YEAR)

    @_('') # empty rule - this fits all the empty reductions
    def empty(self, p):
        return p

    def error(self, p):
        """
            +error()+: attempts to resynchronize at EOL
        """
        tok = p
        if p:
            column = p.index - RRCLexer.last_eol_column
            print("parser error: unexpected token %s (\"%s\") at line %d column %d" % (p.type, p.value, p.lineno, column), file=sys.stderr)
            while True:
                tok = next(self.tokens, None)
                if not tok or tok.type == 'EOL':
                    break
            self.errok()
        else:
            raise ParserError("Unexpected EOF")
        return tok
