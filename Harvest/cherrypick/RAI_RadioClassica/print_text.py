from rrc_pick import RRCPick

collection = RRCPick.manage()
for f in collection:
    for t in f.extract_text():
        for l in t:
            print(l, end='')
