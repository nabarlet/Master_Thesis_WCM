import os
import matplotlib.pyplot as plt

def plotmethod(func):
    """
        @plotmethod is a decorator to manage plot seamlessly
    """
    def inner(*arg):
        (res, plot_name, filename, plotdir) = func(*arg)
        x = range(len(res))
        fig, ax = plt.subplots()
        fig.set_figwidth(15.3)
        fig.set_figheight(11.5)
        plt.plot(x, res)
        plt.title(plot_name)
        plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')

    return inner

def barmethod(func):
    """
        @barmethod is a decorator to manage bar charts seamlessly
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
