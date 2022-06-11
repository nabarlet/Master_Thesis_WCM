import sys
import bbc3_pick as bp

# Usage: python3 main.py [number of records]
# if no number is provided the default is to download all the available tweets

bpt = bp.BBC3Pick()
if len(sys.argv) > 1:
	bpt.limit=int(sys.argv[1])
for r in bpt.parse():
	print(r.inspect())
