import pytest
import solver

SIMPLE_BOARD = [
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0
]

INVALID_BOARD = [
    0, 0, 4,  0, 0, 4,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0
]

INITIAL_BOARD = [
    0, 0, 0,  2, 6, 0,  7, 0, 1,
    6, 8, 0,  0, 7, 0,  0, 9, 0,
    1, 9, 0,  0, 0, 4,  5, 0, 0,

    8, 2, 0,  1, 0, 0,  0, 4, 0,
    0, 0, 4,  6, 0, 2,  9, 0, 0,
    0, 5, 0,  0, 0, 3,  0, 2, 8,

    0, 0, 9,  3, 0, 0,  0, 7, 4,
    0, 4, 0,  0, 5, 0,  0, 3, 6,
    7, 0, 3,  0, 1, 8,  0, 0, 0
]

GOAL_BOARD = [
    4, 3, 5,  2, 6, 9,  7, 8, 1,
    6, 8, 2,  5, 7, 1,  4, 9, 3,
    1, 9, 7,  8, 3, 4,  5, 6, 2,

    8, 2, 6,  1, 9, 5,  3, 4, 7,
    3, 7, 4,  6, 8, 2,  9, 1, 5,
    9, 5, 1,  7, 4, 3,  6, 2, 8,

    5, 1, 9,  3, 2, 6,  8, 7, 4,
    2, 4, 8,  9, 5, 7,  1, 3, 6,
    7, 6, 3,  4, 1, 8,  2, 5, 9
]

TWO_OFF_BOARD = [
    4, 3, 5,  2, 6, 9,  7, 8, 1,
    6, 8, 2,  5, 7, 1,  4, 9, 3,
    1, 9, 7,  8, 3, 4,  0, 6, 2,

    8, 2, 6,  1, 9, 5,  3, 4, 7,
    3, 7, 4,  6, 8, 2,  9, 1, 5,
    9, 5, 0,  7, 4, 3,  6, 2, 8,

    5, 1, 9,  3, 2, 6,  8, 7, 4,
    2, 4, 8,  9, 5, 7,  1, 3, 6,
    7, 6, 3,  4, 1, 8,  2, 5, 9
]

ZERO_WEIGHTS = [0.0] * (9 * 83)


def test_basic_search_raises_no_arguments():
    with pytest.raises(TypeError) as _:
        solver.basic_search()


def test_basic_search_raises_excessive_arguments():
    with pytest.raises(TypeError) as _:
        solver.basic_search(INITIAL_BOARD, INITIAL_BOARD)


def test_basic_search_raises_mishapen_board():
    with pytest.raises(ValueError) as _:
        board = INITIAL_BOARD.copy()
        board.append(0)
        solver.basic_search(board)


def test_basic_search_raises_noninteger_board_values():
    with pytest.raises(TypeError) as _:
        board = INITIAL_BOARD.copy()
        board[0] = 0.0
        solver.basic_search(board)


def test_basic_search_raises_invalid_board():
    with pytest.raises(ValueError) as _:
        solver.basic_search(INVALID_BOARD)


def test_basic_search_two_off():
    goal = solver.basic_search(TWO_OFF_BOARD)
    assert goal == GOAL_BOARD


def test_basic_search_initial():
    goal = solver.basic_search(INITIAL_BOARD)
    assert goal == GOAL_BOARD


def test_heuristic_search_takes_two_arguments():
    with pytest.raises(TypeError) as _:
        solver.evaluate_square_heuristic()
    with pytest.raises(TypeError) as _:
        solver.evaluate_square_heuristic(ZERO_WEIGHTS)
    with pytest.raises(TypeError) as _:
        solver.evaluate_square_heuristic(INITIAL_BOARD)
    with pytest.raises(TypeError) as _:
        solver.evaluate_square_heuristic(ZERO_WEIGHTS, INITIAL_BOARD, 5)


def test_heuristic_search_takes_keyword_args():
    assert solver.evaluate_square_heuristic(weights=ZERO_WEIGHTS, state=INITIAL_BOARD) > 0
    assert solver.evaluate_square_heuristic(state=INITIAL_BOARD, weights=ZERO_WEIGHTS) > 0


def test_heuristic_search_raises_mishapen_weights():
    with pytest.raises(ValueError) as _:
        weights = ZERO_WEIGHTS.copy()
        weights.append(0.0)
        solver.evaluate_square_heuristic(weights, INITIAL_BOARD)


def test_heuristic_search_raises_mishapen_board():
    with pytest.raises(ValueError) as _:
        board = INITIAL_BOARD.copy()
        board.append(0)
        solver.evaluate_square_heuristic(ZERO_WEIGHTS, board)


def test_heuristic_search_raises_invalid_weight_values():
    with pytest.raises(TypeError) as _:
        weights = ZERO_WEIGHTS.copy()
        weights[0] = 0
        solver.evaluate_square_heuristic(weights, INITIAL_BOARD)


def test_heuristic_search_raises_invalid_board_values():
    with pytest.raises(TypeError) as _:
        board = INITIAL_BOARD.copy()
        board[0] = 0.0
        solver.evaluate_square_heuristic(ZERO_WEIGHTS, board)


def test_heuristic_search_raises_invalid_board():
    with pytest.raises(ValueError) as _:
        solver.evaluate_square_heuristic(ZERO_WEIGHTS, INVALID_BOARD)


def test_heuristic_search_two_off():
    count = solver.evaluate_square_heuristic(ZERO_WEIGHTS, TWO_OFF_BOARD)
    assert count > 0


def test_heuristic_search_initial():
    count = solver.evaluate_square_heuristic(ZERO_WEIGHTS, INITIAL_BOARD)
    assert count > 0
