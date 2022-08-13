import sys,os
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rrc_pick import RRCPick
from common.objects import Performance
from common.utilities.bump import Bump

b = Bump()

for rec in RRCPick.create_csv():
    b.bump()
    print(rec.to_csv())
# Performance.clear_performances_of_provider(PROVIDER)
# b.bump('+')
# for found, not_found in RRCPick.create_csv():
#     b.bump()
#     if found:
#         try:
#             #found.insert(PROVIDER)
#             print(found.to_csv())
#         except Exception as e:
#             print(e, file=sys.stderr)
#     else:
#         print(not_found.to_csv(), file=sys.stderr)
