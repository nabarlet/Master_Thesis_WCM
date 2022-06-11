import matplotlib.pyplot as plt
from csv import reader 
import pandas as pd
from objects import Composer
import sys

if len(sys.argv)<1:
	print("usage:python3 plot.py file to plot", file=sys.stderr)

	
file = sys.argv[1]
data = []
with open(file,newline='') as csv_file:
	records = reader(csv_file)
	for row in records:
		data.append(Composer(row[0],row[1],row[2],row[3]))
		
		
def accumulate_mov(data):
	results={}
	for d in data:
		if d.movement in results:
			results[d.movement]['values']+=1
		else:
			results[d.movement]={'values':1} #create dictionary
	return results
	
def accumulate_names(data):
	results={}
	for d in data:
		if d.name in results:
			results[d.name]+=1
		else:
			results[d.name]=1
	return results

movements = accumulate_mov(data)
names = accumulate_names(data)
m_data = pd.DataFrame.from_dict(movements,orient='index')
m_data.head()
#m_data.plot.hist(alpha=0.5)
#plt.show()

#for k,v in movements.items():
#	print("%s: %s" %(k,v))

#for k,v in names.items():
	#print("%s: %s" %(k,v))
	
#plt.hist(names.values())
#plt.show()



	


