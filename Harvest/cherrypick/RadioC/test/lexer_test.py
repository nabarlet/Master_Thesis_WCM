import pdb
import unittest
import os, sys

sys.path.extend(['.', '..'])
from rc_pick import RCPick
from rc_parser.rc_lex import RCLexer

class TestRCLexer(unittest.TestCase):

    def setUp(self):
        self.collection = RCPick.manage()
        self.lexer = RCLexer()

    def test_lexer(self):
        for c in self.collection:
            fn = os.path.basename(c.filename)
            for cl, date, time in c.find_composer_lines():
                for work in RCPick.separate_composers(cl):
                    for t in self.lexer.tokenize(work):
                        # print("%s: %s" % (fn, t))
                        self.assertTrue(t)
            c.pdf.close()

if __name__ == '__main__':
  unittest.main()
