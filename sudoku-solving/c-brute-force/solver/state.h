#ifndef C_BRUTE_FORCE_STATE_H
#define C_BRUTE_FORCE_STATE_H

#include <array>
#include <vector>

namespace solver {

static constexpr int NROWS = 9;
static constexpr int NCOLS = 9;

class State {
 public:
  State(std::array<int, NROWS * NCOLS> state);
  State(const State &);

  bool operator==(const State&) const;

  bool is_goal() const;
  bool is_valid() const;
  bool is_filled_in(int row, int col) const;
  std::string display() const;
  std::vector<State> next_states(int row, int col) const;

 private:
  std::array<int, NROWS * NCOLS> m_state;
};

}

#endif //C_BRUTE_FORCE_STATE_H
