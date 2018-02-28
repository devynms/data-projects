#ifndef PROJECT_PARSE_H
#define PROJECT_PARSE_H

#include <istream>
#include "state.h"

namespace solver {

State parse_state(std::istream& input);

}

#endif //PROJECT_PARSE_H
