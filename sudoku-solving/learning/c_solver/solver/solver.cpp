#include "solver.h"

#include <memory>
#include <vector>
#include <array>
#include <limits>


namespace solver {

int
internal::StateDescription::operator()(idx_type row, idx_type col) const
{
  return m_desc[row * NUM_ROWS + col];
}


int&
internal::StateDescription::operator()(idx_type row, idx_type col)
{
  return m_desc[row * NUM_ROWS + col];
}


bool
internal::StateDescription::operator==(const StateDescription &other) const
{
  return m_desc == other.m_desc;
}


bool
internal::StateDescription::operator!=(const StateDescription &other) const
{
  return !(*this == other);
}


internal::square_iter
internal::squares_begin()
{
  return { 0, 0 };
}


internal::square_iter
internal::squares_end()
{
  return { 10, 10 };
}


internal::square_iter
internal::operator++(const square_iter& pos)
{
  if (pos.row == 8 && pos.col == 8) {
    return { 10, 10 };
  } else if (pos.col == 8) {
    return { pos.row + 1, 0 };
  } else {
    return { pos.row, pos.col + 1 };
  }
}


bool
internal::operator==(const square_iter& lhs, const square_iter& rhs)
{
  return lhs.row == rhs.row && lhs.col == rhs.col;
}


bool
internal::operator!=(const square_iter& lhs, const square_iter& rhs)
{
  return !(lhs == rhs);
}


GameStateBuilder&
GameStateBuilder::set_square(idx_type row, idx_type col, int value)
{
  if (row > 9 || col > 9) {
    return *this;
  }
  bool found_value = false;
  for (auto& square : m_squares) {
    if (square.row == row && square.col == col) {
      square.value = value;
      found_value = true;
    }
  }
  if (!found_value) {
    m_squares.push_back({ row, col, value });
  }
  return *this;
}


GameState
GameStateBuilder::build() const
{
  using internal::StateDescription;

  StateDescription desc;
  for (auto& square : m_squares) {
    desc(square.row, square.col) = square.value;
  }
  return GameState(desc);
}


GameState::GameState(internal::StateDescription state)
    : m_state(state)
{}


bool
GameState::operator==(const GameState &other) const
{
  return m_state == other.m_state;
}


bool
GameState::is_legal() const
{
  constexpr idx_type NUM_BOX_COLS = 3;
  constexpr idx_type NUM_BOX_ROWS = 3;

  for (idx_type row = 0; row < NUM_ROWS; row++) {
    if (row_contains_duplicate(row)) {
      return false;
    }
  }
  for (idx_type col = 0; col < NUM_COLS; col++) {
    if (col_contains_duplicate(col)) {
      return false;
    }
  }
  for (idx_type box_row = 0; box_row < NUM_BOX_ROWS; box_row++) {
    for (idx_type box_col = 0; box_col < NUM_BOX_COLS; box_col++) {
      if (box_contains_duplicate(box_row, box_col)) {
        return false;
      }
    }
  }
  return true;
}


bool
GameState::is_goal() const
{
  for (idx_type row = 0; row < NUM_ROWS; row++) {
    for (idx_type col = 0; col < NUM_COLS; col++) {
      if (!is_filled(row, col)) {
        return false;
      }
    }
  }
  return true;
}


bool
GameState::is_filled(idx_type row, idx_type col) const
{
  return m_state(row, col) != 0;
}


GameState
GameState::next_state(idx_type row, idx_type col, int value) const
{
  using internal::StateDescription;

  StateDescription next_state = m_state;
  next_state(row, col) = value;
  return GameState(next_state);
}


std::vector<GameState>
GameState::next_legal_states(idx_type row, idx_type col) const
{
  constexpr idx_type MAX_NEXT_STATES = 9;

  std::vector<GameState> next_states;
  if (is_filled(row, col)) {
    return next_states;
  }
  next_states.reserve(MAX_NEXT_STATES);
  for (int value = 1; value <= 9; value++) {
    GameState next_game_state = next_state(row, col, value);
    if (next_game_state.is_legal()) {
      next_states.push_back(std::move(next_game_state));
    }
  }
  return next_states;
}


bool
GameState::row_contains_duplicate(idx_type row) const
{
  int value_counts[10] = { 0 };
  for (idx_type col = 0; col < NUM_COLS; col++) {
    value_counts[m_state(row, col)]++;
  }
  for (std::size_t i = 1; i <= 9; i++) {
    if (value_counts[i] > 1) {
      return true;
    }
  }
  return false;
}


bool
GameState::col_contains_duplicate(idx_type col) const
{
  int value_counts[10] = { 0 };
  for (idx_type row = 0; row < NUM_ROWS; row++) {
    value_counts[m_state(row, col)]++;
  }
  for (std::size_t i = 1; i <= 9; i++) {
    if (value_counts[i] > 1) {
      return true;
    }
  }
  return false;
}


bool
GameState::box_contains_duplicate(idx_type box_row, idx_type box_col) const
{
  idx_type row_begin = box_row * 3;
  idx_type row_end = row_begin + 3;
  idx_type col_begin = box_col * 3;
  idx_type col_end = col_begin + 3;
  int value_counts[10] = { 0 };
  for (idx_type row = row_begin; row < row_end; row++) {
    for (idx_type col = col_begin; col < col_end; col++) {
      value_counts[m_state(row, col)]++;
    }
  }
  for (std::size_t i = 1; i <= 9; i++) {
    if (value_counts[i] > 1) {
      return true;
    }
  }
  return false;
}


SearchResults::SearchResults(std::unique_ptr<GameState> goal_state, counter_type count)
  : m_goal_state(std::move(goal_state)),
    m_count(count)
{}


bool
SearchResults::found_solution() const
{
  return m_goal_state != nullptr;
}


counter_type
SearchResults::states_explored() const
{
  return m_count;
}


GameState&
SearchResults::goal_state()
{
  return *m_goal_state;
}


const GameState&
SearchResults::goal_state() const
{
  return *m_goal_state;
}


SearchResults
BruteForceSearch::search(const GameState &initial_state)
{
  std::unique_ptr<GameState> result = this->square_dfs(initial_state, internal::squares_begin());
  return SearchResults(std::move(result), m_count);
}


std::unique_ptr<GameState>
BruteForceSearch::square_dfs(const GameState &state, const internal::square_iter& pos)
{
  m_count += 1;
  if (pos == internal::squares_end()) {
    if (state.is_goal()) {
      return std::make_unique<GameState>(state);
    } else {
      return std::unique_ptr<GameState>();
    }
  }
  if (state.is_filled(pos.row, pos.col)) {
    return square_dfs(state, ++pos);
  }
  auto next_states = state.next_legal_states(pos.row, pos.col);
  if (next_states.size() == 0) {
    return std::unique_ptr<GameState>();
  }
  for (const auto& next_state : next_states) {
    auto result = square_dfs(next_state, ++pos);
    if (result) {
      return result;
    }
  }
  return std::unique_ptr<GameState>();
}


std::vector<int>
SquareHeuristic::operator()(const GameState &state, idx_type row, idx_type col)
{
  arma::mat input(83, 1);
  arma::uword idx = 0;
  for (idx_type row = 0; row < NUM_ROWS; row++) {
    for (idx_type col = 0; col < NUM_COLS; col++) {
      input(idx) = static_cast<double>(state(row, col));
      idx++;
    }
  }
  input(81, 0) = static_cast<double>(row);
  input(82, 0) = static_cast<double>(col);
  arma::mat output = m_theta * input;
  std::vector<int> softmax_values;
  softmax_values.reserve(9);
  for (int i = 0; i < 9; i++) {
    arma::uword max_idx = output.index_max();
    softmax_values.push_back(static_cast<int>(max_idx) + 1);
    output(max_idx) = -std::numeric_limits<double>::infinity();
  }
  return softmax_values;
}

} // namespace solver
