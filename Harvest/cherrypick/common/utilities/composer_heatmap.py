import pdb
import sys, os
import matplotlib.pyplot as plt

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

from common.utilities.composer_plot import ComposerProviderPlot, ComposerFullPlot, ComposerRadioPlot, ComposerMovementPlot
from common.utilities.plot_range import PlotRange
from db.db import DbPro

class ComposerHeatmap:

    __THRESHOLD_PERCENTAGE__ = 0.6
    def calc_labels(self, th_perc = __THRESHOLD_PERCENTAGE__):
        col_sum = self.sorted_keys
        threshold=th_perc
        labels = []
        xs = []
        for idx, cs in enumerate(col_sum):
            if cs[1] >= threshold:
                labels.append(cs[0])
                xs.append(idx)
        return [xs, labels]

    def create_heatmap(self, plot_name, prange = PlotRange(), th_perc = __THRESHOLD_PERCENTAGE__):
        self.plot_range = prange
        result = []
        
        for list_row in self.get_submatrix():
            result.append(list_row)
        (xs,labels) = self.calc_labels(th_perc)
        fig, ax = plt.subplots()
        fig.set_figwidth(25.6)
        fig.set_figheight(19.2)
        im = ax.imshow(result, cmap=plt.cm.RdBu)
        ax.tick_params(axis="x", rotation=90)
        plt.xticks(xs, labels)
        plt.yticks(xs, labels) # use the same for y labels
        plt.colorbar(im)
        plt.title("%s heatmap (range: %s over %d x %d)" % (plot_name, self.plot_range.source, *self.size()))
        plt.grid(color='w', linestyle='-.', linewidth=1.5)
        plt.savefig('%s_heatmap.png' % (plot_name), bbox_inches='tight')

class ComposerGlobalHeatmap(ComposerHeatmap, ComposerFullPlot):

    def __init__(self, db = DbPro()):
        #super(ComposerFullPlot, self).__init__(db)
        super().__init__(db)

    def create_heatmap(self, prange = PlotRange()):
        self.load_map()
        #super(ComposerHeatmap, self).create_heatmap('global', prange)
        super().create_heatmap('global', prange)

class ComposerRadioHeatmap(ComposerHeatmap, ComposerRadioPlot):

    def __init__(self, db = DbPro()):
        super().__init__(db)

    def create_heatmap(self, prange = PlotRange()):
        self.load_map()
        super().create_heatmap('radio only', prange)

class ComposerProviderHeatmap(ComposerHeatmap, ComposerProviderPlot):

    def __init__(self, prov, db = DbPro()):
        super().__init__(db)
        self.provider_name = prov

    def create_heatmap(self, prange = PlotRange()):
        self.load_map(self.provider_name)
        super().create_heatmap(self.provider_name, prange)

class ComposerMovementHeatmap(ComposerHeatmap, ComposerMovementPlot):

    def __init__(self, movement, db = DbPro()):
        super().__init__(db)
        self.movement_name = movement

    def create_heatmap(self, prange = PlotRange()):
        self.load_map(self.movement_name)
        super().create_heatmap(self.movement_name, prange)
