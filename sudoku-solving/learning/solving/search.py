from abc import ABC, abstractmethod
import numpy as np
from itertools import product


class SquareModel(ABC):

    @abstractmethod
    def is_state_goal(self, state):
        pass

    @abstractmethod
    def is_state_filled(self, state, row, col):
        pass

    @abstractmethod
    def is_state_legal(self, state):
        pass

    @abstractmethod
    def next_state(self, state, row, col, value):
        pass

    @abstractmethod
    def heuristic(self, state, row, col):
        pass


class Square:

    SQUARES = [(r, c) for r in range(9) for c in range(9)]

    def __init__(self, idx):
        self._idx = idx

    def next(self):
        if self._idx == (len(Square.SQUARES) - 1):
            return None
        else:
            return Square(self._idx + 1)

    def value(self):
        return Square.SQUARES[self._idx]



class SquareSearchInstance:

    def __init__(self, model):
        self._model = model
        self._count = 0
        self._solution = None

    def search(self, state, square):
        self._count += 1

        if square is None:
            if self._model.is_state_goal(state):
                self._solution = state
                return True
            return False

        row, col = square.value()
        print(f'{row}, {col}')

        if self._model.is_state_filled(state, row, col):
            return self.search(state, square.next())

        for value in self._model.heuristic(state, row, col):
            next_state = self._model.next_state(state, row, col, value)
            if self._model.is_state_legal(next_state) and \
                    self.search(next_state, square.next()):
                return True

        return False


    def states_explored(self):
        return self._count

    def solution(self):
        return self._solution


class SquareSolver:

    def __init__(self, model):
        self._model = model

    def search(self, initial_state):
        instance = SquareSearchInstance(self._model)
        instance.search(initial_state, Square(0))
        return (instance.states_explored(), instance.solution())


class BasicModel(SquareModel):

    def __init__(self):
        pass

    def heuristic(self, state, row, col):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def next_state(self, state, row, col, value):
        next_state = state.copy()
        next_state[row, col] = value
        return next_state

    def is_state_filled(self, state, row, col):
        return state[row, col] != 0

    def is_state_goal(self, state):
        return self.is_state_legal(state) and np.all(state != 0)

    def is_state_legal(self, state):
        if self._contains_block_duplicates(state): return False
        if self._contains_col_duplicates(state): return False
        if self._contains_row_duplicates(state): return False
        return True

    def _contains_row_duplicates(self, state):
        for row in range(9):
            if self._section_contains_duplicates(state[row, :]):
                return True
        return False

    def _contains_block_duplicates(self, state):
        for block_row, block_col in product(range(3), range(3)):
            row_lo = block_row * 3
            row_hi = row_lo + 3
            col_lo = block_col * 3
            col_hi = col_lo + 3
            block = state[row_lo:row_hi, col_lo:col_hi]
            if self._section_contains_duplicates(block):
                return True
        return False

    def _contains_col_duplicates(self, state):
        for col in range(9):
            if self._section_contains_duplicates(state[:, col]):
                return True
        return False

    def _section_contains_duplicates(self, state):
        for value in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            count = np.count_nonzero(state == value)
            if count > 1:
                return True
        return False



def BasicState(state):
    if not len(state) == 9 * 9:
        raise ValueError('State has wrong number of values.')
    return np.matrix(state).reshape((9, 9))


