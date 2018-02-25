import numpy as np

class State:

    # state: 9x9 numpy array
    def __init__(self, state):
        self._state = state

    def __hash__(self):
        code = 17
        for row in self._state:
            for elem in row:
                code = 31 * code + elem
        return code

    def __eq__(self, other):
        if self is other: return True
        if not self.__class__ == other.__class__: return False
        return np.all(self._state == other._state)

    def neighbors(self):
        neighbors = []
        for (row, values) in enumerate(self._state):
            for (col, elem) in enumerate(values):
                if elem == 0:
                    for val in range(1, 10):
                        next_state = _substitute(self._state, row, col, val)
                        if _is_legal(next_state):
                            neighbors.append(next_state)
        return neighbors


def _substitute(state, row, col, val):
    next_state = np.copy(state)
    next_state[row][col] = val

# state: 9x9 numpy array
def _is_legal(state):
    # row can't contain duplicate
    for row in range(1, 10):
        pass
    # column can't contain duplicate
    for col in range(1, 10):
        pass
    # 3x3 box can't contain duplicate
    pass