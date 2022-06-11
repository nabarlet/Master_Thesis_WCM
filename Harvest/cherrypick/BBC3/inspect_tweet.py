import sys
import bbc3_pick as bp

# Usage: python3 inspect_tweet.py [number of records]
# if no number is provided the default is to download all the available tweets

bpt = bp.BBC3Pick()
if len(sys.argv) > 1:
	bpt.limit=int(sys.argv[1])
for tweet in bpt.inspect():
    print(tweet)
