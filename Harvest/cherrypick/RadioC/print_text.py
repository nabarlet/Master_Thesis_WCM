import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.utilities.string import join

from rc_pick import RCPick

collection = RCPick.manage()
for c in collection:
    for txt in c.find_composer_lines():
        print(txt)
