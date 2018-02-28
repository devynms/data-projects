#ifndef C_BRUTE_FORCE_SEARCH_H
#define C_BRUTE_FORCE_SEARCH_H

#include "state.h"

namespace solver {

std::unique_ptr<solver::State>
search(const solver::State &initial_state);

}

#endif //C_BRUTE_FORCE_SEARCH_H
