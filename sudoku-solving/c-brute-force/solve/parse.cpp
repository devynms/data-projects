#include "parse.h"

solver::State
solver::parse_state(std::istream &input) {
  std::array<int, 9*9> values;
  int size = 0;
  while(size < 9 * 9) {
    int value;
    input >> value;
    if (value >= 0 && value <= 9) {
      values[size] = value;
      size++;
    }
  }
  return solver::State(values);
}
