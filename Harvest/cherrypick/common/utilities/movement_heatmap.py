import pdb
import sys, os
import matplotlib.pyplot as plt

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

from common.utilities.movement_plot import MovementPlot
from db.db import DbPro

class MovementHeatmap(MovementPlot):

    def calc_labels(self):
        labels = []
        xs = []
        for idx, cs in enumerate(self.matrix.keys()):
            labels.append(cs)
            xs.append(idx)
        return [xs, labels]

    def create_heatmap(self):
        self.load_map()
        plot_name = 'Movement'
        result = []
        for row in self.matrix.values():
            r_arr = []
            for col in row.values():
                r_arr.append(col)
            result.append(r_arr)
        (xs,labels) = self.calc_labels()
        fig, ax = plt.subplots()
        fig.set_figwidth(25.6)
        fig.set_figheight(19.2)
        im = ax.imshow(result, cmap=plt.cm.RdBu)
        ax.tick_params(axis="x", rotation=90)
        plt.xticks(xs, labels)
        plt.yticks(xs, labels) # use the same for y labels
        plt.colorbar(im)
        plt.title("%s heatmap (%d x %d)" % (plot_name, *self.size()))
        plt.grid(color='w', linestyle='-.', linewidth=1.5)
        plt.savefig('%s_heatmap.png' % (plot_name), bbox_inches='tight')
