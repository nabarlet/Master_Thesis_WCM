import sys,os
import traceback
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#from bbc3_pick import BBC3Pick
from download.collector import Collector
from common.objects import Performance
from common.utilities.bump import Bump

b = Bump()

PROVIDER = 'BBC3'
for sd in Collector.collect(PROVIDER):
    for rec in sd:
        print(rec.to_csv())
        b.bump()
