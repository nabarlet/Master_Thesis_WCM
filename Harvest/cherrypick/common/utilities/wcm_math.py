import pdb
import numpy as np

def gini_coefficient(x):
    """
        gini_coefficient(x)

        - x is a vector

        returns the gini coefficient of vector x (slow concise implementation)

        https://newbedev.com/calculating-gini-coefficient-in-python-numpy
    """
    # (Warning: This is a concise implementation, but it is O(n**2)
    # in time and memory, where n = len(x).  *Don't* pass in huge
    # samples!)

    # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g

def gini_porcaro(x):
    """
    """
    # The rest of the code requires numpy arrays.
    result = None
    try:
        x = np.asarray(x)
        sorted_x = np.sort(x)
        n = len(x)
        cumx = np.cumsum(sorted_x, dtype=float)
        # The above formula, with all weights equal to 1 simplifies to:
        result = (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n
    except:
        print("operation: (%d + 1 - 2 * %f / %f) / %d fails and returns None" % (n, np.sum(cumx), cum[-1], n), file=sys.stderr)
        result = None
    return result

def fast_gini_coefficient(x):
    """
        Compute Gini coefficient of array of values (fast implementation)
        https://newbedev.com/calculating-gini-coefficient-in-python-numpy
    """
    diffsum = 0
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))
    return diffsum / (len(x)**2 * np.mean(x))

def decile(datasize, slices = 10):
    """
        decile(datasize)

        calculates the decile portions of a data set, returning the 
        corresponding set of ten indexes for an equal division
    """
    ar = np.arange(datasize)
    result = [int(n) for n in np.percentile(ar, np.arange(0, slices*10, 10)).round()]
    return result

__INNER_GOLDEN_MEAN__ = 2.0/(1.0+np.sqrt(5))
def exp_decile(datasize, start_slice, end_slice = None, slices = 10):
    """
        exp_decile(datasize, start_slice, end_slice = None, slices = 10)

        calculates the exponential decile portions of a data set, returning the 
        corresponding set of ten indexes for an exponential division (e**(ax+b)).
        If no end_slice is provided, the end_slice will be taken to be the
        golden mean of datasize.
    """
    if not end_slice:
        end_slice = int(np.round(datasize*__INNER_GOLDEN_MEAN__))
    x = np.arange(slices-1)
    rng = x[-1] - x[0]
    a_fact = (np.log(end_slice)-np.log(start_slice))/rng
    b_fact = np.log(start_slice) - (a_fact * x[0])
    result = np.zeros(slices, dtype=int)
    result[1:] = [int(n) for n in np.exp(a_fact*x+b_fact).round()]
    return result
