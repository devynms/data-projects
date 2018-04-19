from sklearn import preprocessing
from itertools import product
import numpy as np


class TrainingSet:

    def __init__(self, data, target):
        self.data = data
        self.target = target

    def __eq__(self, other):
        return \
            self.data == other.data and \
            self.target == other.target

    def __repr__(self):
        return f'TrainingSet(\ndata={repr(self.data)},\ntarget={repr(self.target)}\n)'


def complete(lb, question, solution, row, col):
    q = np.zeros((9*9) + 2, dtype=np.int8)
    i = (row * 9) + col
    # Fill with the solution up to a point
    q[0:i] = solution.flatten()[0:i]
    # The rest of the input is the unfinished board
    q[i:(9*9)] = question.flatten()[i:(9*9)]
    # Add the row and col as input data
    q[(9*9)] = row
    q[(9*9)+1] = col
    # convert to an indicator variable and flatten
    return lb.transform(q).flatten()


def training_set(questions, solutions):
    lb = preprocessing.LabelBinarizer()
    lb.fit(range(10))

    data_rows = len(questions) * 81
    data_cols = 830
    data = np.zeros((data_rows, data_cols))
    pt = 0
    for question, solution in zip(questions, solutions):
        for row, col in product(range(9), range(9)):
            data[pt, :] = complete(lb, question, solution, row, col)
            pt += 1

    target = np.array([
        solution[row, col]
        for question, solution in zip(questions, solutions)
        for row, col in product(range(9), range(9))
    ], dtype=np.int8)
    return TrainingSet(data, target)
