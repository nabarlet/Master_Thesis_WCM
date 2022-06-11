import pdb
import sys, os
import yaml

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*1)), os.path.join(mypath, *(['..']*2))])

from common.utilities.composer_heatmap import ComposerRadioHeatmap
from common.utilities.plot_range       import PlotRange
from db.db import DbDev

prange = PlotRange.create(":120x:120")
if len(sys.argv)>1:
    prange = PlotRange.create(sys.argv[1])
cgh = ComposerRadioHeatmap()
cgh.create_heatmap(prange)
