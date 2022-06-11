import pdb
import os, sys

sys.path.extend(['..', os.path.join('..', '..')])

from common.utilities.path import root_path, test_file
from rrc_parser.sections.recording_parser import RRCRecordingLexer
from rrc_parser.text_conditioner import text_conditioner

f = open('test5.txt', 'r')
text = ''.join(f.readlines())
f.close()


lexer = RRCRecordingLexer()

for t in lexer.tokenize(text):
    print(t)
