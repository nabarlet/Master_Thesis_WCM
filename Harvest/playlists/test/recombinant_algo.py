def print_sum_result(matrix):
    total = 0
    for row, cols in matrix.items():
        for col, value in cols.items():
            total += value
    gauss_total = (len(matrix) * (len(matrix)-1))/2.0
    print(total, ' (gauss series) -> ', gauss_total)

def recombinant_algo(arr, result):
    sz = len(arr)
    off = 0
    while (sz >= 1):
        for idx, key in enumerate(arr[off:]):
            idx1 = off
            idx2 = off+idx
            if idx1 != idx2:
                r = arr[idx1]
                c = arr[idx2]
                result[r][c] += 1
                result[c][r] += 1
        off += 1
        sz  -= 1

def matrix_fill(combinations):
    matrix = {k:None for k in combinations[0]} # combinations[0] holds the largest combination
    for k in matrix.keys():
        matrix[k] = {k:0 for k in combinations[0]} # ditto
    for arr in combinations:
        recombinant_algo(arr, matrix)

    print(matrix)
    print_sum_result(matrix)

if __name__ == '__main__':
    combinations = [\
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], \
        ['A', 'B', 'C', 'D', 'E', 'F', 'G'], \
        ['A', 'B', 'C', 'D', 'E', 'F'], \
        ['A', 'B', 'C', 'D', 'E'], \
        ['A', 'B', 'C', 'D'], \
        ['A', 'B', 'C'], \
        ['A', 'B'], \
        ['A'], \
    ]
    matrix_fill(combinations)
