#include <iostream>
#include "state.h"
#include "parse.h"
#include "search.h"

int main(int argc, char* argv[]) {
  using namespace solver;
  using namespace std;

  State initial_state = parse_state(cin);
  cout << "Solving..." << endl;
  unique_ptr<State> goal_state = search(initial_state);
  if (goal_state) {
    cout << "Found goal state.\n" << goal_state->display() << endl;
  } else {
    cout << "No goal state found.\n";
  }

  return 0;
}
