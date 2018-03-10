#include "solver.h"


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


internal::square_iter&
internal::operator++(square_iter& pos)
{
  if (pos.row == 8 && pos.col == 8) {
    pos =  { 10, 10 };
  } else if (pos.col == 8) {
    pos =  { pos.row + 1, 0 };
  } else {
    pos = { pos.row, pos.col + 1 };
  }
  return pos;
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


std::unique_ptr<GameState>
internal::square_dfs(const GameState &state, internal::square_iter pos)
{
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
  // value_counts[X-1] = # of times the number X appeared
  int value_counts[9] = { 0 };
  for (idx_type col = 0; col < NUM_COLS; col++) {
    value_counts[m_state(row, col) - 1]++;
  }
  for (std::size_t i = 0; i < 9; i++) {
    if (value_counts[i] > 1) {
      return true;
    }
  }
  return false;
}


bool
GameState::col_contains_duplicate(idx_type col) const
{
  // value_counts[X-1] = # of times the number X appeared
  int value_counts[9] = { 0 };
  for (idx_type row = 0; row < NUM_ROWS; row++) {
    value_counts[m_state(row, col) - 1]++;
  }
  for (std::size_t i = 0; i < 9; i++) {
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
  // value_counts[X-1] = # of times the number X appeared
  int value_counts[9] = { 0 };
  for (idx_type row = row_begin; row < row_end; row++) {
    for (idx_type col = col_begin; col < col_end; col++) {
      value_counts[m_state(row, col) - 1]++;
    }
  }
  for (std::size_t i = 0; i < 9; i++) {
    if (value_counts[i] > 1) {
      return true;
    }
  }
  return false;
}


SearchResults::SearchResults(std::unique_ptr<GameState> goal_state)
  : m_goal_state(std::move(goal_state))
{}


bool
SearchResults::found_solution() const
{
  return m_goal_state != nullptr;
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
search(const GameState& initial_state)
{
  std::unique_ptr<GameState> result = internal::square_dfs(initial_state, internal::squares_begin());
  return SearchResults(std::move(result));
}


} // namespace solver
