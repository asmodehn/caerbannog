import enum

import pytest
from hypothesis import given, infer
from hypothesis.strategies import sampled_from

try:
    from .. import function
except (ValueError, ImportError):
    import fun.purity.function as function


@given(v=infer)
def test_int_function(v: int):

    @function.function()
    def inc_forty_two(arg: int) -> int:
        return 42 + arg

    # check mapping is a correct abstraction
    m = {}

    m.setdefault(v, inc_forty_two(v))

    # check calling it multiple times gives the same result

    # CAREFUL with identity /vs/ equality

    # Verify identity
    # assert inc_forty_two(v) is m[v]
    # False for basic types ( or in general ?)

    # Verify equality
    assert inc_forty_two(v) == m[v]


@given(v=infer)
def test_int_nonfunction(v: int):
    const = 42

    @function.function()
    def inc_forty_two(arg: int) -> int:
        nonlocal const
        return const + arg

    # check mapping is a correct abstraction
    m = {}

    m.setdefault(v, inc_forty_two(v))

    # changes const
    const = 33

    # check calling it now raises an exception
    with pytest.raises(function.ImpureFunction):
        inc_forty_two(v)


class ETest(enum.Enum):
    A = 1
    B = 2
    C = 3

    def next_elem(self):
        return ETest((self.value % 3) + 1)


@given(v=sampled_from(ETest))
def test_enum_function(v: ETest):

    @function.function()
    def next_enum(arg: ETest) -> ETest:
        return arg.next_elem()

    # check mapping is a correct abstraction
    m = {}

    m.setdefault(v, next_enum(v))

    # check calling it multiple times gives the same result

    # CAREFUL with identity /vs/ equality

    # Verify identity
    # assert inc_forty_two(v) is m[v]
    # False for basic types ( or in general ?)

    # Verify equality
    assert next_enum(v) == m[v]


@given(v=sampled_from(ETest))
def test_enum_nonfunction(v: ETest):
    change = 0

    @function.function()
    def next_enum(arg: ETest) -> ETest:
        return ETest(1 + ((arg.next_elem().value + change) % 3))

    # TODO : check cache size

    # check mapping is a correct abstraction
    m = {}

    m.setdefault(v, next_enum(v))

    # changes
    change = 1

    # check calling it now raises an exception
    with pytest.raises(function.ImpureFunction):
        next_enum(v)































if __name__ == '__main__':
    pytest.main(['-s', __file__])
