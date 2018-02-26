import pytest
import numpy as np
from solver.state import State

#
# Definitions
#

NUMROWS = 9
NUMCOLS = 9
NUMVALUES = 9

#
# Tests
#

def test_next_state():
    initial_state = State(np.zeros((NUMROWS, NUMCOLS)))
    neighbors = initial_state.neighbors()
    assert len(neighbors) == (NUMROWS * NUMCOLS * NUMVALUES)
    arr = np.zeros((NUMROWS, NUMCOLS))
    arr[0][0] = 1
    expected = State(arr)
    assert expected in neighbors
