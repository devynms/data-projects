import numpy as np
from sklearn import preprocessing

from solving.search import BasicModel, BasicState


class LogitModel(BasicModel):

    def __init__(self):
        super().__init__()
        self._lb = preprocessing.LabelBinarizer()
        self._lb.fit(range(10))

    def heuristic(self, state, row, col):
        repr = np.zeros((9*9) + 2)
        repr[0:(9*9)] = state.flatten()
        repr[(9*9)] = row
        repr[(9*9) + 1] = col
        x = self._lb.transform(repr)

def LogitState(state):
    return BasicState(state)