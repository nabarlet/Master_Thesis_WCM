import os, sys

sys.path.extend(['.', '..'])
from rc_pick import RCPick
from rc_parser.rc_lex import RCLexer

collection = RCPick.manage()
lexer = RCLexer()

for c in collection:
    for txt in c.extract_relevant_text():
        for t in lexer.tokenize(txt):
            print(t)
