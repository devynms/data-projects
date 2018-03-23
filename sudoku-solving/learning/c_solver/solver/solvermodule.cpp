#include <Python.h>
#include "solver.h"

#include <armadillo>
#include <vector>

static std::unique_ptr<arma::mat> _solver_parse_weights(PyObject*);
static std::unique_ptr<solver::GameState> _solver_parse_state(PyObject*);

static PyObject*
solver_basic_search(PyObject* self, PyObject* args)
{
  PyObject* seq;
  if (!PyArg_ParseTuple(args, "O", &seq)) {
    return NULL;
  }

  if (!PySequence_Check(seq)) {
    PyErr_SetString(PyExc_TypeError, "Expected a sequence.");
    return NULL;
  }

  Py_ssize_t len = PySequence_Length(seq);
  if (len != (solver::NUM_ROWS * solver::NUM_COLS)) {
    PyErr_SetString(PyExc_ValueError, "Incorrect number of values.");
    return NULL;
  }

  std::vector<int> values;
  values.reserve(solver::NUM_ROWS * solver::NUM_COLS);
  for (Py_ssize_t idx = 0; idx < len; idx++) {
    PyObject* value_obj = PySequence_GetItem(seq, idx);
    if (!PyLong_Check(value_obj)) {
      PyErr_SetString(PyExc_TypeError, "Expected sequence elements to be integral.");
      return NULL;
    }
    long value = PyLong_AsLong(value_obj);
    if (PyErr_Occurred()) {
      return NULL;
    }
    if (value < 0 || value > 9) {
      PyErr_SetString(PyExc_ValueError, "Expected sequence values to be in range [0, 9].");
      return NULL;
    }
    values.push_back(static_cast<int>(value));
  }

  const solver::GameState initial_state = solver::GameState::from_collection(std::begin(values), std::end(values));
  if (!initial_state.is_legal()) {
    PyErr_SetString(PyExc_ValueError, "Provided sequence does not describe a legal board.");
    return NULL;
  }

  const solver::SearchResults results = solver::BruteForceSearch().search(initial_state);
  if (!results.found_solution()) {
    Py_RETURN_NONE;
  }

  const solver::GameState& goal_state = results.goal_state();
  PyObject* py_result = PyList_New(len);
  if (py_result == NULL) {
    return NULL;
  }
  Py_ssize_t idx = 0;
  for (solver::idx_type row = 0; row < solver::NUM_ROWS; row++) {
    for (solver::idx_type col = 0; col < solver::NUM_COLS; col++) {
      PyList_SET_ITEM(py_result, idx, PyLong_FromLong(goal_state(row, col)));
      idx += 1;
    }
  }
  return py_result;
}

static PyObject*
solver_evaluate_square_heuristic(PyObject* self, PyObject* args, PyObject* keywds)
{
  static char* kwlist[] = { (char*) "weights", (char *) "state" };
  PyObject* weights_seq;
  PyObject* state_seq;
  if (!PyArg_ParseTupleAndKeywords(args, keywds, "OO", kwlist, &weights_seq, &state_seq)) {
    return NULL;
  }
  std::unique_ptr<arma::mat> weights = _solver_parse_weights(weights_seq);
  if (!weights) {
    return NULL;
  }
  std::unique_ptr<solver::GameState> initial_state = _solver_parse_state(state_seq);
  if (!initial_state) {
    return NULL;
  }
  auto results = solver::HeuristicSquareSearch(std::move(*weights)).search(*initial_state);
  auto states_explored = results.states_explored();
  PyObject* result = PyLong_FromLong(static_cast<long>(states_explored));
  return result;
}

static PyMethodDef SolverMethods[] = {
    {
        "basic_search",
        solver_basic_search,
        METH_VARARGS,
        "Basic search function."
    },
    {
        "evaluate_square_heuristic",
        (PyCFunction) solver_evaluate_square_heuristic,
        METH_VARARGS | METH_KEYWORDS,
        "Evaluate a square heuristic against a given instance of a search."
    },
    { NULL, NULL, 0, NULL } // sentinel
};


static struct PyModuleDef solvermodule = {
    PyModuleDef_HEAD_INIT,
    "solver",
    NULL,
    -1,
    SolverMethods
};


PyMODINIT_FUNC
PyInit_solver(void)
{
  return PyModule_Create(&solvermodule);
}

std::unique_ptr<arma::mat>
_solver_parse_weights(PyObject* seq)
{
  if (!PySequence_Check(seq)) {
    PyErr_SetString(PyExc_TypeError, "Provided weights must be a sequence.");
    return nullptr;
  }
  Py_ssize_t length = PySequence_Length(seq);
  if (length != (83 * 9)) {
    PyErr_SetString(PyExc_ValueError, "Provided weights did not have expected shape.");
    return nullptr;
  }
  arma::mat weight_matrix(9, 83);
  Py_ssize_t idx = 0;
  for (auto& elem : weight_matrix) {
    PyObject* py_weight = PySequence_GetItem(seq, idx);
    if (!PyFloat_Check(py_weight)) {
      PyErr_SetString(PyExc_TypeError, "Expected elements of weight matrix to be floating point.");
      return nullptr;
    }
    double weight = PyFloat_AsDouble(py_weight);
    if (PyErr_Occurred()) {
      return nullptr;
    }
    elem = weight;
    idx++;
  }
  return std::make_unique<arma::mat>(std::move(weight_matrix));
}

std::unique_ptr<solver::GameState>
_solver_parse_state(PyObject* seq)
{
  using solver::GameState;
  using namespace std;

  if (!PySequence_Check(seq)) {
    PyErr_SetString(PyExc_TypeError, "Provided game state must be a sequence.");
    return nullptr;
  }
  Py_ssize_t len = PySequence_Length(seq);
  if (len != solver::NUM_ROWS * solver::NUM_COLS) {
    PyErr_SetString(PyExc_ValueError, "Provided game state must have the correct number of values.");
    return nullptr;
  }
  vector<int> values;
  values.reserve(solver::NUM_ROWS * solver::NUM_COLS);
  for (Py_ssize_t idx = 0; idx < len; idx++) {
    PyObject* value_obj = PySequence_GetItem(seq, idx);
    if (!PyLong_Check(value_obj)) {
      PyErr_SetString(PyExc_TypeError, "Expected sequence elements to be integral.");
      return nullptr;
    }
    long value = PyLong_AsLong(value_obj);
    if (PyErr_Occurred()) {
      return nullptr;
    }
    if (value < 0 || value > 9) {
      PyErr_SetString(PyExc_ValueError, "Expected sequence values to be in range [0, 9].");
      return nullptr;
    }
    values.push_back(static_cast<int>(value));
  }
  GameState state = GameState::from_collection(begin(values), end(values));
  if (!state.is_legal()) {
    PyErr_SetString(PyExc_ValueError, "Initial state must be a valid sudoku board.");
    return nullptr;
  }
  return make_unique<GameState>(move(state));
}

