from rrc_pick import RRCPick

collection = RRCPick.manage()
for f in collection:
    for obj in f.parse():
        print(obj.inspect())
