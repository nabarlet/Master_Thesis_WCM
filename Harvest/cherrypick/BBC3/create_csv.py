import sys,os
import traceback
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bbc3_pick import BBC3Pick
from common.objects import Performance
from common.utilities.bump import Bump

b = Bump()

PROVIDER = 'BBC3'
Performance.clear_performances_of_provider(PROVIDER)
b.bump('+')
for found, not_found in BBC3Pick.create_csv():
    b.bump()
    if found:
        try:
            found.insert(PROVIDER)
            print(found.to_csv())
        except Exception as e:
            print("\"%s\" raised an exception: %s" % (found.inspect(), e), file=sys.stderr)
            (type, value, tb) = sys.exc_info()
            traceback.print_tb(tb, file=sys.stderr)
    else:
        print(not_found.to_csv(), file=sys.stderr)
