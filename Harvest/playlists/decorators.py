import os
import matplotlib.pyplot as plt
import pdb

__RUNNING_AVERAGE_SIZE__ = 100
def running_average(data):
    sz = len(data)
    results = []
    start = 0
    end   = __RUNNING_AVERAGE_SIZE__ 
    while (start < sz):
        avg = 0
        for d in data[start:end]:
            avg += d
        avg /= __RUNNING_AVERAGE_SIZE__
        results.extend([avg]*__RUNNING_AVERAGE_SIZE__)
        start = end + 1
        if len(data[start:]) > __RUNNING_AVERAGE_SIZE__:
            end += __RUNNING_AVERAGE_SIZE__
        else:
            end += len(data[start:])
    return results

def plotmethod(func):
    """
        @plotmethod is a decorator to manage plot seamlessly
    """
    def inner(*arg):
        (res, plot_name, filename, plotdir) = func(*arg)
        x = range(len(res))
        ravg = running_average(res)
        xavg = range(len(ravg))
        fig, ax = plt.subplots()
        fig.set_figwidth(15.3)
        fig.set_figheight(11.5)
        plt.plot(x, res)
        plt.plot(xavg, ravg, linewidth=4)
        plt.ylim(0.0, 0.5)
        plt.title(plot_name)
        plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')

    return inner

def vbarmethod(func):
    """
        @vbarmethod is a decorator to manage bar charts seamlessly (vertical)
    """
    def inner(*arg):
        (xlabels, y, plot_name, filename, plotdir) = func(*arg)
        x = range(len(y))
        fig, ax = plt.subplots()
        fig.set_figwidth(15.3)
        fig.set_figheight(11.5)
        ax.tick_params(axis="x", rotation=90)
        plt.bar(x, y)
        plt.xticks(x, xlabels)
        plt.title(plot_name)
        plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')

    return inner
    
def hbarmethod(func):
    """
        @hbarmethod is a decorator to manage bar charts seamlessly (horizontal)
    """
    def inner(*arg):
        (ylabels, y, plot_name, filename, plotdir) = func(*arg)
        x = range(len(y))
        fig, ax = plt.subplots()
        fig.set_figwidth(11.5)
        fig.set_figheight(15.3)
        plt.barh(y,x)
        plt.yticks(x, ylabels)
        plt.title(plot_name)
        plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')

    return inner
