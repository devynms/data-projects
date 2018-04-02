from abc import ABC, abstractmethod
import numpy as np


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

    SQUARES = [(r, c) for r in range(0, 10) for c in range(0, 10)]

    def __init__(self, idx):
        self._idx = 0

    def next(self):
        if self._idx == len(Square.SQUARES) - 1:
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
            return False
        if self._model.is_state_goal(state):
            self._solution = state
            return True
        row, col = square.value()
        if self._model.is_state_filled(state, row, col):
            return self.search(state, square.next())
        for value in self._model.heuristic(state, row, col):
            next_state = self._model.next_state(state, row, col, value)
            if self._model.is_state_legal(state) and \
                    self.search(next_state, square.next()):
                return True
        return False


    def states_explored(self):
        return self._count

    def solution(self):
        return self._solution


class Solution:

    def __init__(self, states_explored, solution):
        self.states_explored = states_explored
        self.solution = solution


class SquareSolver:

    def __init__(self, model):
        self._model = model

    def search(self, initial_state):
        instance = SquareSearchInstance(self._model)
        instance.search(initial_state, Square(0))
        return Solution(instance.states_explored(), instance.solution())


class BasicModel(SquareModel):

    def heuristic(self, state, row, col):
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def next_state(self, state, row, col, value):
        next_state = state.copy()
        next_state[row, col] = value
        return next_state

    def is_state_filled(self, state, row, col):
        return state[row, col] != 0

    def is_state_goal(self, state):
        return self.is_state_legal(state) and np.all(state == 0)

    def is_state_legal(self, state):
        pass


def BasicState(state):
    if not len(state) == 9 * 9:
        raise ValueError('State wrong number of values')
    return np.matrix(state).reshape((9, 9))


