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

std::unique_ptr<solver::State>
dfs(const solver::State &state, int row, int col) {
  count++;
  if (count % 100000 == 0) {
    std::cout << "States explored: ~" << (count / 1000)  << "K\r" << std::flush;
  }

  if (row == -1) {
    if (state.is_goal()) {
      return std::make_unique<solver::State>(state);
    } else {
      return std::unique_ptr<solver::State>{};
    }
  }
  auto neighbors = state.next_states(row, col);
  int nr = next_row(row, col);
  int nc = next_col(row, col);
  if (state.is_filled_in(row, col)) {
    // proceed if already filled in
    return dfs(state, nr, nc);
  } else if (neighbors.size() == 0) {
    // backtrack if can't explore
    return std::unique_ptr<solver::State>{};
  } else {
    for (const auto &neighbor : neighbors) {
      auto result = dfs(neighbor, nr, nc);
      if (result) {
        return result;
      }
    }
    return std::unique_ptr<solver::State>{};
  }
}

std::unique_ptr<solver::State>
solver::search(const solver::State &initial_state) {
  std::unique_ptr<solver::State> result = dfs(initial_state, 0, 0);
  std::cout << "Found solution by exploring " << count << " states.\n";
  return result;
}
