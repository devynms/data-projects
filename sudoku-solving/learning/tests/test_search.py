from solving.search import *


SIMPLE_STATE = BasicState([
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,

  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,

  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0
])


INVALID_STATE = BasicState([
  0, 0, 4,  0, 0, 4,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,

  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,

  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0
])


INITIAL_STATE = BasicState([
  0, 0, 0,  2, 6, 0,  7, 0, 1,
  6, 8, 0,  0, 7, 0,  0, 9, 0,
  1, 9, 0,  0, 0, 4,  5, 0, 0,

  8, 2, 0,  1, 0, 0,  0, 4, 0,
  0, 0, 4,  6, 0, 2,  9, 0, 0,
  0, 5, 0,  0, 0, 3,  0, 2, 8,

  0, 0, 9,  3, 0, 0,  0, 7, 4,
  0, 4, 0,  0, 5, 0,  0, 3, 6,
  7, 0, 3,  0, 1, 8,  0, 0, 0
])


GOAL_STATE = BasicState([
  4, 3, 5,  2, 6, 9,  7, 8, 1,
  6, 8, 2,  5, 7, 1,  4, 9, 3,
  1, 9, 7,  8, 3, 4,  5, 6, 2,

  8, 2, 6,  1, 9, 5,  3, 4, 7,
  3, 7, 4,  6, 8, 2,  9, 1, 5,
  9, 5, 1,  7, 4, 3,  6, 2, 8,

  5, 1, 9,  3, 2, 6,  8, 7, 4,
  2, 4, 8,  9, 5, 7,  1, 3, 6,
  7, 6, 3,  4, 1, 8,  2, 5, 9
])


TWO_OFF_STATE = BasicState([
  4, 3, 5,  2, 6, 9,  7, 8, 1,
  6, 8, 2,  5, 7, 1,  4, 9, 3,
  1, 9, 7,  8, 3, 4,  0, 6, 2,

  8, 2, 6,  1, 9, 5,  3, 4, 7,
  3, 7, 4,  6, 8, 2,  9, 1, 5,
  9, 5, 0,  7, 4, 3,  6, 2, 8,

  5, 1, 9,  3, 2, 6,  8, 7, 4,
  2, 4, 8,  9, 5, 7,  1, 3, 6,
  7, 6, 3,  4, 1, 8,  2, 5, 9
])


def test_squares():
  assert len(Square.SQUARES) == 9 * 9
  assert Square(9*9 - 1).next() is None


def test_basic_model_is_legal():
  model = BasicModel()
  assert model.is_state_legal(SIMPLE_STATE)
  assert not model.is_state_legal(INVALID_STATE)
  assert model.is_state_legal(INITIAL_STATE)
  assert model.is_state_legal(GOAL_STATE)
  assert model.is_state_legal(TWO_OFF_STATE)


def test_basic_model_next_state():
  model = BasicModel()
  next_state = model.next_state(SIMPLE_STATE, 0, 0, 1)
  assert model.is_state_legal(next_state) is True
  assert next_state[0, 0] == 1


def test_basic_model_state_filled():
  model = BasicModel()
  assert not model.is_state_filled(INITIAL_STATE, 0, 0)
  assert model.is_state_filled(INITIAL_STATE, 1, 0)


def test_basic_model_is_goal():
  model = BasicModel()
  assert not model.is_state_goal(SIMPLE_STATE)
  assert not model.is_state_goal(INVALID_STATE)
  assert not model.is_state_goal(INITIAL_STATE)
  assert model.is_state_goal(GOAL_STATE)
  assert not model.is_state_goal(TWO_OFF_STATE)


def test_solver_basic_search():
  model = BasicModel()
  solver = SquareSolver(model)
  (count, goal) = solver.search(TWO_OFF_STATE)
  assert count > 0
  assert model.is_state_goal(goal)


def test_solver_deeper_search():
  model = BasicModel()
  solver = SquareSolver(model)
  (count, goal) = solver.search(INITIAL_STATE)
  assert count > 0
  assert model.is_state_goal(goal)
