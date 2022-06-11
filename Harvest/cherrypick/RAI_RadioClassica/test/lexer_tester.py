import pdb
import os, sys

sys.path.extend(['..', os.path.join('..', '..')])

from common.utilities.path import root_path, test_file
from rrc_parser.rrc_lex import RRCLexer, LexicalError
from rrc_parser.text_conditioner import text_conditioner

f = open('full_text.txt', 'r')
text = ''.join(f.readlines())
f.close()


lexer = RRCLexer()

tokens = lexer.tokenize(text)
print("generator created")

for t in tokens:
    print(t)
