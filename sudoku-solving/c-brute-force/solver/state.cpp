#include "state.h"
#include <sstream>

using namespace solver::state;

static constexpr int NVALUES = 9;
static constexpr int BOX_NROWS = 3;
static constexpr int BOX_NCOLS = 3;
static constexpr int NBOX_ROWS = 3;
static constexpr int NBOX_COLS = 3;

static int
get(const std::array<int, NCOLS * NROWS> &array, int row, int col) {
  return array[row * NROWS + col];
}

static bool
rows_valid(const std::array<int, NROWS * NCOLS> &state) {
  for (int row = 0; row < NROWS; row++) {
    int counts[NVALUES] = {0};
    for (int col = 0; col < NCOLS; col++) {
      int value = get(state, row, col);
      if (value != 0) {
        counts[value - 1]++;
      }
    }
    for (int i = 0; i < NVALUES; i++) {
      if (counts[i] > 1) {
        return false;
      }
    }
  }
  return true;
}

static bool
cols_valid(const std::array<int, NROWS * NCOLS> &state) {
  for (int col = 0; col < NCOLS; col++) {
    int counts[NVALUES] = {0};
    for (int row = 0; row < NROWS; row++) {
      int value = get(state, row, col);
      if (value != 0) {
        counts[value - 1]++;
      }
    }
    for (int i = 0; i < NVALUES; i++) {
      if (counts[i] > 1) {
        return false;
      }
    }
  }
  return true;
}

static bool
box_valid(const std::array<int, NROWS * NCOLS> &state, int boxrow, int boxcol) {
  int counts[NVALUES] = {0};
  for (int row = boxrow * 3; row < boxrow * 3 + BOX_NROWS; row++) {
    for (int col = boxcol * 3; col < boxcol * 3 + BOX_NCOLS; col++) {
      int value = get(state, row, col);
      if (value != 0) {
        counts[value - 1]++;
      }
    }
  }
  for (int i = 0; i < NVALUES; i++) {
    if (counts[i] > 1) {
      return false;
    }
  }
  return true;
}

static bool
boxes_valid(const std::array<int, NROWS * NCOLS> &state) {
  for (int boxrow = 0; boxrow < NBOX_ROWS; boxrow++) {
    for (int boxcol = 0; boxcol < NBOX_COLS; boxcol++) {
      if (!box_valid(state, boxrow, boxcol)) {
        return false;
      }
    }
  }
  return true;
}

static bool
is_state_valid(const std::array<int, NROWS * NCOLS> &state) {
  return rows_valid(state) &&
      cols_valid(state) &&
      boxes_valid(state);
}

State::State(std::array<int, NROWS * NCOLS> state)
    : m_state(state) {}

std::vector<State>
State::next_states(int row, int col) const {
  if (get(m_state, row, col) == 0) {
    std::vector<State> neighbors;
    neighbors.reserve(NVALUES);
    for (int value = 1; value <= 9; value++) {
      std::array<int, NROWS * NCOLS> state = m_state;
      state[row * NROWS + col] = value;
      if (is_state_valid(state)) {
        neighbors.emplace_back(state);
      }
    }
    return neighbors;
  } else {
    return std::vector<State>();
  }
}

bool
State::is_goal() const {
  for (int value : m_state) {
    if (value == 0) {
      return false;
    }
  }
  return true;
}

State::State(const State &that)
    : m_state(that.m_state) {}

bool
State::is_valid() const {
  return is_state_valid(m_state);
}

bool
State::operator==(const State& other) const {
  for (int i = 0; i < NROWS * NCOLS; i++) {
    if (m_state[i] != other.m_state[i]) {
      return false;
    }
  }
  return true;
}

std::string State::display() const {
  std::ostringstream os;
  os << "State:\n";
  for (int i = 0; i < NROWS * NCOLS; i++) {
    if (i % 27 == 26) {
      os << m_state[i] << "\n\n";
    } else if (i % 9 == 8) {
      os << m_state[i] << "\n";
    } else if (i % 3 == 2) {
      os << m_state[i] << "  ";
    } else  {
      os << m_state[i] << " ";
    }
  }
  return os.str();
}

