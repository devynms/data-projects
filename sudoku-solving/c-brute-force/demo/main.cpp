#include <iostream>
#include "state.h"
#include "search.h"

using solver::State;
using solver::search;

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

int main() {

  std::unique_ptr<State> solution = search(INITIAL_STATE);

  if (solution) {
    std::cout << "\nSolution found!\n";
    std::cout << solution->display() << std::endl;
  } else {
    std::cout << "\nNo solution found.\n";
  }
}