import pytest
import numpy as np
from solver.state import State

#
# Definitions
#

NUMROWS = 9
NUMCOLS = 9
NUMVALUES = 9

INITIAL_STATE = np.matrix([
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
])

GOAL_STATE = np.matrix([
    [4, 3, 5, 2, 6, 9, 7, 8, 1],
    [6, 8, 2, 5, 7, 1, 4, 9, 3],
    [1, 9, 7, 8, 3, 4, 5, 6, 2],
    [8, 2, 6, 1, 9, 5, 3, 4, 7],
    [3, 7, 4, 6, 8, 2, 9, 1, 5],
    [9, 5, 1, 7, 4, 3, 6, 2, 8],
    [5, 1, 9, 3, 2, 6, 8, 7, 4],
    [2, 4, 8, 9, 5, 7, 1, 3, 6],
    [7, 6, 3, 4, 1, 8, 2, 5, 9]
])

#
# Tests
#

def test_simple_next_state():
    simple_state = State(np.zeros((NUMROWS, NUMCOLS)))
    neighbors = simple_state.all_neighbors()
    assert len(neighbors) == (NUMROWS * NUMCOLS * NUMVALUES)
    arr = np.zeros((NUMROWS, NUMCOLS))
    arr[0][0] = 1
    expected = State(arr)
    assert expected in neighbors

def test_initial_next_state():
    initial_state = State(INITIAL_STATE)
    neighbors = initial_state.all_neighbors()
    assert 0 < len(neighbors) < (NUMROWS * NUMCOLS * NUMVALUES)

def test_rc_neighbors():
    initial_state = State(INITIAL_STATE)
    neighbors = initial_state.neighbors(0, 0)
    for value in range(1, 10):
        arr = INITIAL_STATE.copy()
        arr[0, 0] = value
        expected_state = State(arr)
        if value in {3, 4, 5}:
            assert expected_state in neighbors
        else:
            assert expected_state not in neighbors

def test_state_is_legal():
    initial_state = State(INITIAL_STATE)
    goal_state = State(GOAL_STATE)
    arr = np.zeros((NUMCOLS, NUMROWS))
    arr[0, 0] = 1
    arr[0, 1] = 1
    bad_state = State(arr)
    assert initial_state.is_legal()
    assert goal_state.is_legal()
    assert not bad_state.is_legal()

def test_state_is_goal():
    initial_state = State(INITIAL_STATE)
    goal_state = State(GOAL_STATE)
    assert not initial_state.is_goal()
    assert goal_state.is_goal()


def test_row_col_neighbors():
    initial_state = State(np.zeros((NUMROWS, NUMCOLS)))
    neighbors = initial_state.neighbors(0, 0)
    arr = np.zeros((NUMROWS, NUMCOLS))
    for value in range(1, 10):
        arr[0, 0] = value
        assert State(arr) in neighbors
