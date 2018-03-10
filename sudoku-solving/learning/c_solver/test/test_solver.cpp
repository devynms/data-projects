#include "solver.h"

#include <vector>
#include <algorithm>
#include <memory>

#include "gtest/gtest.h"

using solver::GameState;
using solver::internal::StateDescription;
using solver::SearchResults;


static StateDescription SIMPLE_DESCRIPTION({
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,

  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,

  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0
});

static GameState SIMPLE_STATE(SIMPLE_DESCRIPTION);


static StateDescription INVALID_DESCRIPTION({
  0, 0, 4,  0, 0, 4,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,

  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,

  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 0,  0, 0, 0,  0, 0, 0
});

static GameState INVALID_STATE(INVALID_DESCRIPTION);


static StateDescription INITIAL_DESCRIPTION({
  0, 0, 0,  2, 6, 0,  7, 0, 1,
  6, 8, 0,  0, 7, 0,  0, 9, 0,
  1, 9, 0,  0, 0, 4,  5, 0, 0,

  8, 2, 0,  1, 0, 0,  0, 4, 0,
  0, 0, 4,  6, 0, 2,  9, 0, 0,
  0, 5, 0,  0, 0, 3,  0, 2, 8,

  0, 0, 9,  3, 0, 0,  0, 7, 4,
  0, 4, 0,  0, 5, 0,  0, 3, 6,
  7, 0, 3,  0, 1, 8,  0, 0, 0
});

static GameState INITIAL_STATE(INITIAL_DESCRIPTION);


static StateDescription GOAL_DESCRIPTION({
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

static GameState GOAL_STATE(GOAL_DESCRIPTION);


static StateDescription TWO_OFF_DESCRIPTION({
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

static GameState TWO_OFF_STATE(TWO_OFF_DESCRIPTION);


TEST(TestStateDescription, SameStateEquals) {
  EXPECT_EQ(GOAL_DESCRIPTION, GOAL_DESCRIPTION);
}

TEST(TestStateDescription, SameStateNotEquals) {
  EXPECT_NE(GOAL_DESCRIPTION, INITIAL_DESCRIPTION);
}

TEST(TestStateDescription, IndexOperator) {
  EXPECT_EQ(TWO_OFF_DESCRIPTION(0, 0), 4);
  EXPECT_EQ(TWO_OFF_DESCRIPTION(8, 8), 9);
  EXPECT_EQ(TWO_OFF_DESCRIPTION(3, 6), 3);
}

TEST(TestStateDescription, IndexSet) {
  StateDescription uut(SIMPLE_DESCRIPTION);
  uut(0, 0) = 5;
  EXPECT_EQ(uut(0, 0), 5);
}


TEST(TestSquareIter, SquareIteratorEquals) {
  using solver::internal::square_iter;

  square_iter lhs = { 0, 0 };
  square_iter rhs = { 0, 0 };
  EXPECT_EQ(lhs, rhs);

  lhs = { 1, 8 };
  rhs = { 1, 8 };
  EXPECT_EQ(lhs, rhs);
}

TEST(TestSquareIter, SquareIteratorNotEquals) {
  using solver::internal::square_iter;

  square_iter lhs = { 0, 0 };
  square_iter rhs = { 8, 8 };
  EXPECT_NE(lhs, rhs);

  lhs = { 5, 3 };
  rhs = { 3, 5 };
  EXPECT_NE(lhs, rhs);
}

TEST(TestSquareIter, SquareIterSequence) {
  std::vector<solver::internal::square_iter> expected_sequence = {
      {0, 0}, {0, 1}, {0, 2},  {0, 3}, {0, 4}, {0, 5},  {0, 6}, {0, 7}, {0, 8},
      {1, 0}, {1, 1}, {1, 2},  {1, 3}, {1, 4}, {1, 5},  {1, 6}, {1, 7}, {1, 8},
      {2, 0}, {2, 1}, {2, 2},  {2, 3}, {2, 4}, {2, 5},  {2, 6}, {2, 7}, {2, 8},

      {3, 0}, {3, 1}, {3, 2},  {3, 3}, {3, 4}, {3, 5},  {3, 6}, {3, 7}, {3, 8},
      {4, 0}, {4, 1}, {4, 2},  {4, 3}, {4, 4}, {4, 5},  {4, 6}, {4, 7}, {4, 8},
      {5, 0}, {5, 1}, {5, 2},  {5, 3}, {5, 4}, {5, 5},  {5, 6}, {5, 7}, {5, 8},

      {6, 0}, {6, 1}, {6, 2},  {6, 3}, {6, 4}, {6, 5},  {6, 6}, {6, 7}, {6, 8},
      {7, 0}, {7, 1}, {7, 2},  {7, 3}, {7, 4}, {7, 5},  {7, 6}, {7, 7}, {7, 8},
      {8, 0}, {8, 1}, {8, 2},  {8, 3}, {8, 4}, {8, 5},  {8, 6}, {8, 7}, {8, 8},
  };
  auto expected_itr = std::begin(expected_sequence);
  auto actual_itr = solver::internal::squares_begin();
  while (expected_itr != std::end(expected_sequence) && actual_itr != solver::internal::squares_end()) {
    EXPECT_EQ(*expected_itr, actual_itr);
    ++expected_itr;
    ++actual_itr;
  }
  EXPECT_EQ(expected_itr, std::end(expected_sequence));
  EXPECT_EQ(actual_itr, solver::internal::squares_end());
}


TEST(TestGameStateBuilder, MakeFromCollection) {
  std::vector<int> board = {
      0, 0, 0,  1, 2, 3,  4, 5, 6,
      0, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 0,  0, 0, 0,  0, 0, 0,

      9, 8, 7,  6, 5, 4,  3, 2, 1,
      0, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 0,  0, 0, 0,  0, 0, 0,

      0, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 0,  0, 0, 0,  0, 0, 0,
  };
  GameState state = GameState::from_collection(std::begin(board), std::end(board));
  EXPECT_EQ(state(0, 3), 1);
  EXPECT_EQ(state(3, 0), 9);
}

TEST(TestGameStateBuilder, BuildsEmptyState) {
  GameState state = GameState::builder().build();
  EXPECT_EQ(state, SIMPLE_STATE);
}

TEST(TestGameStateBuilder, BuildsComplexState) {
  GameState state = GameState::builder().set_square(0, 2, 4).set_square(0, 5, 4).build();
  EXPECT_EQ(state, INVALID_STATE);
}


TEST(TestGameState, IndexOperator) {
  EXPECT_EQ(INITIAL_STATE(0, 0), 0);
  EXPECT_EQ(INITIAL_STATE(3, 7), 4);
  EXPECT_EQ(INITIAL_STATE(8, 0), 7);
}

TEST(TestGameState, StatesEqual) {
  GameState lhs(INITIAL_STATE);
  GameState rhs(INITIAL_STATE);
  EXPECT_EQ(lhs, rhs);
}

TEST(TestGameState, StatesNotEqual) {
  GameState lhs(INITIAL_STATE);
  GameState rhs(GOAL_STATE);
  EXPECT_NE(lhs, rhs);
}

TEST(TestGameState, StateIsLegal) {
  EXPECT_TRUE(GOAL_STATE.is_legal());
}

TEST(TestGameState, StateNotLegal) {
  EXPECT_FALSE(INVALID_STATE.is_legal());
}

TEST(TestGameState, StateIsGoal) {
  EXPECT_TRUE(GOAL_STATE.is_goal());
}

TEST(TestGameState, StateNotGoal) {
  EXPECT_FALSE(INITIAL_STATE.is_goal());
}

TEST(TestGameState, IndexFilled) {
  EXPECT_TRUE(INITIAL_STATE.is_filled(1, 0));
}

TEST(TestGameState, IndexNotFilled) {
  EXPECT_FALSE(INITIAL_STATE.is_filled(0, 0));
}

TEST(TestGameState, SingleNextState) {
  GameState next_state = SIMPLE_STATE.next_state(0, 0, 1);
  EXPECT_TRUE(next_state.is_legal());
  EXPECT_EQ(next_state(0, 0), 1);
}

TEST(TestGameState, LegalNextStatesSimpleCase) {
  std::vector<GameState> next_states = SIMPLE_STATE.next_legal_states(0, 0);
  for (int value = 1; value <= 9; value++) {
    auto res = std::find_if(std::begin(next_states), std::end(next_states), [value](const auto& state){
      return state(0, 0) == value;
    });
    EXPECT_NE(res, std::end(next_states)) << "Expected next state to have value " << value;
  }
}

TEST(TestGameState, LegalNextStatesInitialState) {
  std::vector<GameState> next_states = INITIAL_STATE.next_legal_states(0, 0);
  for (const auto& state : next_states) {
    EXPECT_TRUE(state.is_legal());
  }
  for (int value = 3; value <= 5; value++) {
    auto res = std::find_if(std::begin(next_states), std::end(next_states), [value](const auto& state){
      return state(0, 0) == value;
    });
    EXPECT_NE(res, std::end(next_states)) << "Expected next state to have value " << value;
  }
}

TEST(TestGameState, LegalNextStatesEmptyResult) {
  std::vector<GameState> next_states = INITIAL_STATE.next_legal_states(0, 3);
  EXPECT_EQ(next_states.size(), 0);
}


TEST(TestSearchResults, NoFoundSolution) {
  SearchResults uut(nullptr);
  EXPECT_FALSE(uut.found_solution());
}

TEST(TestSearchResults, FoundSolution) {
  SearchResults uut(std::make_unique<GameState>(GOAL_STATE));
  EXPECT_TRUE(uut.found_solution());
}

TEST(TestSearchResults, GetSolution) {
  SearchResults uut(std::make_unique<GameState>(GOAL_STATE));
  ASSERT_TRUE(uut.found_solution());
  EXPECT_EQ(uut.goal_state(), GOAL_STATE);
}


TEST(TestSearch, TwoOffSearch) {
  SearchResults results = solver::search(TWO_OFF_STATE);
  ASSERT_TRUE(results.found_solution());
  EXPECT_EQ(results.goal_state(), GOAL_STATE);
}