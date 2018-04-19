import solver
import numpy as np
from random import sample


def search(board):
    assert board.shape == (9, 9)
    result = solver.basic_search(list(map(int, np.nditer(board))))
    return np.reshape(result, (9, 9))


def evaluate(weights, board):
    assert weights.shape == (9, 83)
    assert board.shape == (9, 9)
    c_weights = list(map(float, np.nditer(weights, order='F')))
    c_board = list(map(int, np.nditer(board)))
    return solver.evaluate_square_heuristic(c_weights, c_board)


def errs(q, w):
    return np.average(list(map(lambda b: evaluate(w, b), sample(q, 1000))))


def climb_hill(q):
    w = np.zeros((9, 83))
    for i in range(1000):
        dws = np.random.rand(1000, 9, 83)
        nws = w + dws
        errs = np.ndarray(list(map(ferr, nws)))
        print(f'error ({i}): {np.min(errs)}')
        w = nws[np.argmin(errs)]
    return w
