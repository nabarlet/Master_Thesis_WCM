import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from bbc3_downloader import BBC3Downloader

# Usage: python3 create_csv.py [number of records]
# if no number is provided the default is to download all the available tweets

bpt = BBC3Downloader()
if len(sys.argv) > 1:
	bpt.limit=int(sys.argv[1])
for found, not_found in bpt.parse():
    if found:
	    print(found.composer.to_csv())
    if not_found:
        print(not_found.composer.to_csv())
