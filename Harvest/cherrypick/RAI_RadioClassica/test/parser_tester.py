import pdb
import os, sys
sys.path.extend(['..', os.path.join('..', '..')])

from rrc_parser.rrc_subdivider import RRCSubdivider
from common.utilities.path import root_path, test_file, full_file
from common.utilities.string import join

f = open('full_text.txt', 'r')

rs = RRCSubdivider(f.readlines())
f.close()

result = rs.parse()
for p in result:
    print(p.inspect())
