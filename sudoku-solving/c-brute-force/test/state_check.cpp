#include "gtest/gtest.h"
#include "state.h"

using solver::State;

static State SIMPLE_STATE({
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,

    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 0,  0, 0, 0,  0, 0, 0
});

static State INVALID_STATE({
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

static State INITIAL_STATE({
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

TEST(SolverState, StateIsValid) {
    EXPECT_TRUE(SIMPLE_STATE.is_valid());
    EXPECT_FALSE(INVALID_STATE.is_valid());
    EXPECT_TRUE(INITIAL_STATE.is_valid());
    EXPECT_TRUE(GOAL_STATE.is_valid());
    EXPECT_TRUE(TWO_OFF.is_valid());
}

TEST(SolverState, StateIsGoal) {
    EXPECT_FALSE(SIMPLE_STATE.is_goal());
    EXPECT_FALSE(INITIAL_STATE.is_goal());
    EXPECT_TRUE(GOAL_STATE.is_goal());
    EXPECT_FALSE(TWO_OFF.is_goal());
}

TEST(SolverState, StateNextStates) {
    auto simple_next_states = SIMPLE_STATE.next_states(0, 0);
    EXPECT_EQ(simple_next_states.size(), 9);
    auto initial_next_states = INITIAL_STATE.next_states(0, 0);
    EXPECT_EQ(initial_next_states.size(), 3);
}

TEST(SolverState, UniquePtrStateOperatorEquals) {
    std::unique_ptr<State> lhs = std::make_unique<State>(GOAL_STATE);
    std::unique_ptr<State> rhs = std::make_unique<State>(GOAL_STATE);
    EXPECT_TRUE(*lhs == *rhs);
}
