import pdb
from rrc_parser.rrc_subdivider import RRCSubdivider
from rrc_pick import RRCPick

collection = RRCPick.manage()
for f in collection:
    for text in f.extract_text():
        rs = RRCSubdivider(text)
        rs.create_sections()
        for s in rs.ignored_sections:
            print(s + '\n')
