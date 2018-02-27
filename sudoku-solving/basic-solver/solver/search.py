from itertools import product
from sys import stdout

count = 0


def search(initial_state):
    return _dfs(initial_state, list(product(range(9), range(9))))


def _dfs(state, depth):
    global count
    count = count + 1
    if count % 1000 == 0:
        stdout.write(f'[Progress] {count}\r')

    if depth == []:
        if state.is_goal():
            return state
        else:
            return None
    (row, col) = depth[0]
    next_depth = depth[1:]
    neighbors = state.neighbors(row, col)
    if neighbors == []:
        return _dfs(state, next_depth)
    else:
        for neighbor in neighbors:
            result = _dfs(neighbor, next_depth)
            if result is not None:
                return result
        return None
