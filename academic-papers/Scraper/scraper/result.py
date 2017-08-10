import re
from inspect import signature

def result_of(obj):
    return _Result(Result.SUCCESS, [obj])


def error_of(obj):
    return _Result(Result.ERROR, obj)


class Result:
    SUCCESS = 'success'
    ERROR = 'error'

    TYPES = { SUCCESS, ERROR }


class _Result:

    def __init__(self, type, inner):
        if type not in Result.TYPES:
            raise ValueError(f'{type} is not one of {Result.TYPES}')
        self.type = type
        self._inner = inner

    # pipeline('v:r')
    def with_obj(self, obj):
        if self.type == Result.SUCCESS:
            inner = self._inner.copy()
            inner.append(obj)
            return _Result(Result.SUCCESS, inner)
        else:
            return self

    def with_result(self, result):
        if self.type == Result.SUCCESS and result.type == Result.SUCCESS:
            return _Result(Result.SUCCESS, self._inner + result._inner)
        elif self.type == Result.ERROR:
            return self
        else:
            return result

    def filter(self, pattern):
        if not re.fullmatch(r'(\*|_)*', pattern):
            raise ValueError(f'{pattern} is not a valid filter pattern')
        if self.type == Result.ERROR:
            return self
        if len(pattern) != len(self._inner):
            raise ValueError(f'{pattern} has length {len(pattern)}, '
                             f'but result only has {len(self._inner)} '
                             f'objects.')
        inner = []
        for (flag, obj) in zip(pattern, self._inner):
            if flag == '*':
                inner.append(obj)
        return _Result(Result.SUCCESS, inner)

    def get(self):
        """Should be wrapped in type check"""
        return self._inner


def track(format):
    """Decorates a function of some format and transforms it into one which
    is a function of Result -> Result.

    Format examples:
        R:R (ex: process result)
        V:R (ex: process one value, may fail)
        V:V (ex: process one value, won't fail)
        VVV:R (ex: process many values, may fail)
        V3:R (ex: process many values, may fail, same as above)
        V:N (ex: store value)
        R:N (ex: log error)
    """
    split = format.split(':')
    if len(split) != 2:
        raise ValueError(
            f'{format} is not a valid track format: '
            f'there should only be one separator')

    (left, right) = split

    multivalue_fmt = re.compile(r'V+')
    countvalue_fmt = re.compile(r'(V)(\d+)')
    result_fmt = re.compile(r'R')
    none_fmt = re.compile(r'N')

    if multivalue_fmt.fullmatch(left):
        input_type = 'V'
        input_count = len(left)
    elif countvalue_fmt.fullmatch(left):
        input_type = 'V'
        input_count = int(left[1:])
    elif result_fmt.fullmatch(left):
        input_type = 'R'
        input_count = 1
    else:
        raise ValueError(f'{left} is not a valid input format')

    if multivalue_fmt.fullmatch(right):
        output_type = 'V'
        output_count = len(right)
    elif countvalue_fmt.fullmatch(right):
        output_type = 'V'
        output_count = int(right[1:])
    elif result_fmt.fullmatch(right):
        output_type = 'R'
        output_count = 1
    elif none_fmt.fullmatch(right):
        output_type = 'N'
        output_count = 1
    else:
        raise ValueError(f'{right} is not a valid output format')

    def decorator(function):
        sig = signature(function)

        if len(sig.parameters) != input_count:
            raise ValueError(
                f'Format {format} taking {input_count} arguments'
                f'is incompatible with function {function.__name__}'
                f'taking {len(sig.parameters)} arguments.')

        def track_function(result):
            if not isinstance(result, _Result):
                raise ValueError(
                    f'Input to track function must be a Result object, '
                    f'{type(result).__name__} provided.')

            if input_type == 'V':
                if result.type == Result.SUCCESS:
                    output = function(*result.get())
                else:
                    return result
            elif input_type == 'R':
                output = function(result)

            if output_type == 'V':
                if isinstance(output, tuple):
                    return _Result(Result.SUCCESS, list(output))
                else:
                    return _Result(Result.SUCCESS, [output])
            elif output_type == 'R':
                return output
            elif output_type == 'N':
                return result

        return track_function

    return decorator
