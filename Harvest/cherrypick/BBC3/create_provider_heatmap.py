import pdb
import sys, os
import yaml

mypath = os.path.dirname(__file__)
sys.path.append('..')

from common.utilities.composer_heatmap import ComposerProviderHeatmap
from common.utilities.plot_range       import PlotRange

prange = PlotRange.create(":120x:120")
if len(sys.argv)>1:
    prange = PlotRange.create(sys.argv[1])
PROVIDER = 'BBC3'
ch = ComposerProviderHeatmap(PROVIDER)
ch.create_heatmap(prange)
#print(ch.to_csv())
