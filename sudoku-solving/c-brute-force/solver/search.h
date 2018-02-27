#ifndef C_BRUTE_FORCE_SEARCH_H
#define C_BRUTE_FORCE_SEARCH_H

#include "state.h"

namespace solver {
namespace search {


    std::unique_ptr<solver::state::State>
    search(const solver::state::State& initial_state);

}
}

#endif //C_BRUTE_FORCE_SEARCH_H
