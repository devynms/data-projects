#
# Test imports
#

import context

#
# UUT
#

from result import result_of, error_of, Result, track

#
# Utility functions
#

def initial_success(val):
    return result_of(val)


def initial_error():
    return error_of('bad request')


@track('V:V')
def double(a):
    return a * 2


@track('V:R')
def if_even_double(a):
    if a % 2 == 0:
        return result_of(a * 2)
    else:
        return error_of('not even')


@track('VV:V')
def add(a, b):
    return a + b

#
# Unit tests
#

def test_with_obj_runs_through_error():
    res = error_of('error')
    res = res.with_obj(3)
    assert res.type == Result.ERROR
    assert res.get() == 'error'


def test_track_vv_runs_through_error():
    res = error_of('error')
    res = double(res)
    assert res.type == Result.ERROR
    assert res.get() == 'error'


def test_track_runs_through_success():
    res = initial_success(4)
    res = if_even_double(res)
    assert res.type == Result.SUCCESS
    [val] = res.get()
    assert val == 8
    res = res.with_obj(3)
    res = add(res)
    assert res.type == Result.SUCCESS
    [val] = res.get()
    assert val == 11


def test_track_runs_through_initial_error():
    res = initial_error()
    res = if_even_double(res)
    assert res.type == Result.ERROR
    val = res.get()
    assert val == 'bad request'
    res = res.with_obj(3)
    assert res.type == Result.ERROR
    val = res.get()
    assert val == 'bad request'
    res = add(res)
    assert res.type == Result.ERROR
    val = res.get()
    assert val == 'bad request'


def test_track_runs_though_intermediate_error():
    res = initial_success(3)
    res = if_even_double(res)
    assert res.type == Result.ERROR
    assert res.get() == 'not even'
    res = res.with_obj(3)
    assert res.type == Result.ERROR
    assert res.get() == 'not even'
    res = add(res)
    assert res.type == Result.ERROR
    assert res.get() == 'not even'
