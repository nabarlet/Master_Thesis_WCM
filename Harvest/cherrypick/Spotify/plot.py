import matplotlib.pyplot as plt
from csv import reader 
import pandas as pd
import sys
import matplotlib.pyplot as plt

if len(sys.argv)<1:
    print("usage:python3 plot.py file to plot", file=sys.stderr)

    
file = sys.argv[1]
composers = {}
with open(file,newline='') as csv_file:
    records = reader(csv_file, delimiter="\t")
    idx = 0
    for row in records:
        if idx == 0:
            idx += 1
            continue
        composer = row[3]
        if not composer in composers:
            composers[composer] = 0
        composers[composer] += 1
        idx += 1

sorted_composers=list(sorted(composers.items(),key= lambda x:x[1], reverse=True))
thresholds = [100, 50, 25,0]
divided_composers={}
last_t=1e6

for t in thresholds:
	divided_composers[t]=[]
	for c,v in sorted_composers:
		if v <= last_t and v>t:
			divided_composers[t].append((c,v))
	last_t=t

for k, a in divided_composers.items():
	labels=[comp[0] for comp in a]
	values=[comp[1] for comp in a]
	plt.figure(figsize=(16,16))
	plt.pie(values,labels=labels)
	plt.title("Composers with > %d occurrencies" %(k))
	plt.savefig("Composers_over_%d.png" %(k))
	#for c,v in a:
		#print("%03d %-50s\t%4d" % (k, c + ":", v))
    
