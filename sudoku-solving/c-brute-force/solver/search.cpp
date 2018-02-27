#include <iostream>
#include "search.h"

static int count = 0;

static int
next_row(int row, int col) {
  if (col == 8) {
    if (row < 8) {
      return row + 1;
    } else {
      return -1;
    }
  } else {
    return row;
  }
}

static int
next_col(int row, int col) {
  if (col < 8) {
    return col + 1;
  } else {
    return 0;
  }
}

std::unique_ptr<solver::state::State>
dfs(const solver::state::State &state, int row, int col) {
  if (row == -1) {
    if (state.is_goal()) {
      return std::make_unique<solver::state::State>(state);
    } else {
      return std::unique_ptr<solver::state::State>{};
    }
  }
  auto neighbors = state.next_states(row, col);
  int nr = next_row(row, col);
  int nc = next_col(row, col);
  if (neighbors.size() == 0) {
    return dfs(state, nr, nc);
  } else {
    for (const auto &neighbor : neighbors) {
      auto result = dfs(neighbor, nr, nc);
      if (result) {
        return result;
      }
    }
    return std::unique_ptr<solver::state::State>{};
  }
}

std::unique_ptr<solver::state::State>
solver::search::search(const solver::state::State &initial_state) {
  return dfs(initial_state, 0, 0);
}
