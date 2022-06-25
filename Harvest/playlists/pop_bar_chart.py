import pdb
import matplotlib.pyplot as plt

cache = '__playlist_cache__'

values = []
with open(cache, 'r') as fh:
    for line in fh:
        (nid, pop, name, mov, cross) = line.split('|')
        values.append(pop)

plt.bar(range(len(values[0:99])), values[0:99])
plt.savefig('./pop_bar_chart.png')
