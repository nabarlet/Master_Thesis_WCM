import pdb
import matplotlib.pyplot as plt

cache = '__playlist_cache__'

values = []
with open(cache, 'r') as fh:
    for line in fh:
        (nid, pop, name, mov, cross) = line.split('|')
        pop = float(pop)
        values.append(pop)
        print("%-40s %14.12f" % (name + '(' + nid + ')', pop))

plt.bar(range(len(values[:1000])), values[:1000])
plt.savefig('./pop_bar_chart.png')
