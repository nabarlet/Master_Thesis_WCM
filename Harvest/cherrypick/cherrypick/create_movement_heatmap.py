import pdb
import sys, os
import yaml

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*1)), os.path.join(mypath, *(['..']*2))])

from common.utilities.movement_heatmap import MovementHeatmap

mh = MovementHeatmap()
mh.create_heatmap()
