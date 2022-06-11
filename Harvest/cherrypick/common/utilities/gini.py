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
