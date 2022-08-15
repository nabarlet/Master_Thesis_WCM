import pdb
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rc_pick import RCPick
from common.objects import Performance
from common.utilities.bump import Bump

b = Bump()

PROVIDER = 'RadioC'
for rec in RCPick.create_csv():
    b.bump()
    print(rec.to_csv())
# for found, not_found in RCPick.create_csv():
#     b.bump()
#     if found:
#         try:
# #           found.insert(PROVIDER)
#             print(found.to_csv())
#         except Exception as e:
#             print(e, file=sys.stderr)
#     if not_found:
#         print(not_found.to_csv(), file=sys.stderr)
