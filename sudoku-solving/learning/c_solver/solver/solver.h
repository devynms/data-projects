#ifndef PROJECT_SOLVER_H
#define PROJECT_SOLVER_H

#include <cstddef>
#include <array>
#include <vector>
#include <memory>
#include <cstdint>

namespace solver {


class GameState;
class GameStateBuilder;

using idx_type = std::size_t;
using counter_type = std::int_fast64_t;

static constexpr idx_type NUM_ROWS = 9;
static constexpr idx_type NUM_COLS = 9;


namespace internal {

class StateDescription {
 public:
  using desc_type = std::array<int, NUM_ROWS * NUM_COLS>;

  StateDescription() : m_desc() {}
  StateDescription(desc_type desc) : m_desc(desc) {}
  StateDescription(const StateDescription& other) : m_desc(other.m_desc) {}

  int operator()(idx_type row, idx_type col) const;
  int& operator()(idx_type row, idx_type col);
  bool operator==(const StateDescription& other) const;
  bool operator!=(const StateDescription& other) const;

 private:
  desc_type m_desc;
};


struct StateSquare {
  idx_type row;
  idx_type col;
  int value;
};


struct square_iter {
  idx_type row;
  idx_type col;
};

square_iter squares_begin();
square_iter squares_end();
square_iter operator++(const square_iter&);
bool operator==(const square_iter&, const square_iter&);
bool operator!=(const square_iter&, const square_iter&);

} // namespace solver::internal


class GameStateBuilder {
 public:
  GameStateBuilder() {}

  GameState build() const;

  GameStateBuilder& set_square(idx_type row, idx_type col, int value);

 private:
  std::vector<internal::StateSquare> m_squares;
};


class GameState {
 public:
  static GameStateBuilder builder() { return GameStateBuilder(); }

  template <typename iterator_type>
  static GameState from_collection(const iterator_type& begin, const iterator_type& end);

  GameState(internal::StateDescription state);
  GameState(const GameState& other) : m_state(other.m_state) {}

  bool operator==(const GameState& other) const;
  bool operator!=(const GameState& other) const { return !(*this == other); }
  int operator()(idx_type row, idx_type col) const { return m_state(row, col); }

  bool is_legal() const;
  bool is_goal() const;
  bool is_filled(idx_type row, idx_type col) const;
  GameState next_state(idx_type row, idx_type col, int value) const;
  std::vector<GameState> next_legal_states(idx_type row, idx_type col) const;

 private:
  friend class GameStateBuilder;

  bool row_contains_duplicate(idx_type row) const;
  bool col_contains_duplicate(idx_type col) const;
  bool box_contains_duplicate(idx_type box_row, idx_type box_col) const;

  internal::StateDescription m_state;
};


class SearchResults {
 public:
  SearchResults(std::unique_ptr<GameState> goal_state, counter_type count);

  bool found_solution() const;
  counter_type states_explored() const;
  GameState& goal_state();
  const GameState& goal_state() const;

 private:
  std::unique_ptr<GameState>  m_goal_state;
  counter_type                m_count;
};


class SearchInterface {
 public:
  virtual SearchResults search(const GameState& initial_state) = 0;
};


class BruteForceSearch : public SearchInterface {
 public:
  BruteForceSearch() : m_count(0) {}
  BruteForceSearch(const BruteForceSearch&) = default;
  BruteForceSearch(BruteForceSearch&&) = default;
  BruteForceSearch& operator=(const BruteForceSearch&) = default;
  BruteForceSearch& operator=(BruteForceSearch&&) = default;

  SearchResults search(const GameState& initial_state) override;

 private:
  std::unique_ptr<GameState> square_dfs(const GameState& state, const internal::square_iter& pos);

  counter_type m_count;
};


} // namespace solver


//
// Template Definitions
//


template <typename iterator_type>
solver::GameState
solver::GameState::from_collection(const iterator_type& begin, const iterator_type& end)
{
  using desc_type = solver::internal::StateDescription::desc_type;

  idx_type count = 0;
  iterator_type it = begin;
  desc_type desc;
  while (count < NUM_ROWS * NUM_COLS && it != end) {
    desc[count] = *it;
    ++count;
    ++it;
  }
  return solver::GameState(solver::internal::StateDescription(desc));
}

#endif //PROJECT_SOLVER_H
