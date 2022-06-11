import pdb
import sys,os
sys.path.append('..')

from rc_pick import RCPick

for c in RCPick.manage():
    for found in c.inspect():
        print(found)
