import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.utilities.string import join

from rc_pick import RCPick

collection = RCPick.manage()
for c in collection:
    txt = c.extract_text_from_pdf()
    print(txt)
