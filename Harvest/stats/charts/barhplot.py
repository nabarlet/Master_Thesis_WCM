import sys,os
import matplotlib.pyplot as plt

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *['..']*2, 'cherrypick'))

from common.utilities.string import string_shortener

def barhplot(y, ylabels, filename_template, title, limit = 60, xlimit = None, plotdir = '.', fontsize=None):
    ylabels = [string_shortener(str(yl)) for yl in ylabels]
    y.reverse()
    ylabels.reverse()
    x = range(len(y))
    fig, ax = plt.subplots()
    fig.set_figwidth(11.5)
    fig.set_figheight(15.3)
    if fontsize:
        plt.rc('font', size=fontsize)
    plt.barh(x,y)
    plt.yticks(x, ylabels)
    if limit:
        title = title % (limit)
        filename_template = filename_template % (limit)
    plt.title(title)
    if xlimit and limit:
        plt.axis([0, xlimit, -1, limit+1])
    filename = filename_template
    plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')
