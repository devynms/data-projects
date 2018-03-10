#include <Python.h>
#include "solver.h"


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

  const solver::SearchResults results = solver::search(initial_state);
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


static PyMethodDef SolverMethods[] = {
    { "basic_search", solver_basic_search, METH_VARARGS, "Basic search function." },
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

