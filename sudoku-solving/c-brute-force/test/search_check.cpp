#include "gtest/gtest.h"

#include "state.h"
#include "search.h"

using solver::State;
using solver::search;

static State GOAL_STATE ({
  4, 3, 5,  2, 6, 9,  7, 8, 1,
  6, 8, 2,  5, 7, 1,  4, 9, 3,
  1, 9, 7,  8, 3, 4,  5, 6, 2,

  8, 2, 6,  1, 9, 5,  3, 4, 7,
  3, 7, 4,  6, 8, 2,  9, 1, 5,
  9, 5, 1,  7, 4, 3,  6, 2, 8,

  5, 1, 9,  3, 2, 6,  8, 7, 4,
  2, 4, 8,  9, 5, 7,  1, 3, 6,
  7, 6, 3,  4, 1, 8,  2, 5, 9
});

static State TWO_OFF({
  4, 3, 5,  2, 6, 9,  7, 8, 1,
  6, 8, 2,  5, 7, 1,  4, 9, 3,
  1, 9, 7,  8, 3, 4,  0, 6, 2,

  8, 2, 6,  1, 9, 5,  3, 4, 7,
  3, 7, 4,  6, 8, 2,  9, 1, 5,
  9, 5, 0,  7, 4, 3,  6, 2, 8,

  5, 1, 9,  3, 2, 6,  8, 7, 4,
  2, 4, 8,  9, 5, 7,  1, 3, 6,
  7, 6, 3,  4, 1, 8,  2, 5, 9
});

std::string display(const std::unique_ptr<State>& state) {
  if (state) {
    return state->display();
  } else {
    return "NONE";
  }
}

TEST(SolverSearch, SearchTwoOff) {
  std::unique_ptr<State> result = search(TWO_OFF);
  std::unique_ptr<State> expected = std::make_unique<State>(GOAL_STATE);
  ASSERT_NE(result, nullptr);
  EXPECT_EQ(*result, *expected)
            << "Expected " << display(result) << " to equal " << display(expected);
}
