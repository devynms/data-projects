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
        if self is other:
            return True
        if not self.__class__ == other.__class__:
            return False
        return np.all(self._state == other._state)

    def __str__(self):
        return f'State{{{self._state}}}'

    def all_neighbors(self):
        neighbors = []
        for (row, values) in enumerate(self._state):
            for (col, elem) in enumerate(values):
                if elem == 0:
                    for val in range(1, 10):
                        next_state = _substitute(self._state, row, col, val)
                        if _is_legal(next_state):
                            neighbors.append(State(next_state))
        return neighbors

    def neighbors(self, row, col):
        neighbors = []
        elem = self._state[row, col]
        for value in range(1, 10):
            next_state = _substitute(self._state, row, col, value)
            if _is_legal(next_state):
                neighbors.append(State(next_state))
        return neighbors


def _substitute(state, row, col, val):
    next_state = np.copy(state)
    next_state[row,col] = val
    return next_state


# state: 9x9 numpy array
def _is_legal(state):
    if _rows_contain_duplicate(state):
        return False
    if _cols_contain_duplicate(state):
        return False
    if _boxes_contain_duplicate(state):
        return False
    return True


def _rows_contain_duplicate(state):
    for row in range(0, 9):
        for value in range(1, 10):
            if (state[row,:] == value).sum() > 1:
                return True
    return False


def _cols_contain_duplicate(state):
    for col in range(0, 9):
        for value in range(1, 10):
            if (state[:,col] == value).sum() > 1:
                return True
    return False


def _boxes_contain_duplicate(state):
    for row in range(0, 3):
        for col in range(0, 3):
            if _box_contains_duplicate(state, row, col):
                return True
    return False


def _box_contains_duplicate(state, row, col):
    rowleft = row * 3
    rowright = rowleft + 3
    colleft = col * 3
    colright = colleft + 3
    box = state[rowleft:rowright, colleft:colright]
    for value in range(1, 10):
        if (box == value).sum() > 1:
            return True
    return False
