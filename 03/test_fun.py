import copy

import pytest
import fun


#@pytest.mark.skip
def test_const():

    c = fun.Map(42)

    assert c() == 42


#@pytest.mark.skip
def test_applicable_lambda():

    a = fun.Map(lambda: 42)

    assert a() == 42


#@pytest.mark.skip
def test_applicable_function():

    def answer():
        return 42

    f = fun.Map(answer)

    assert f() == 42


def test_1arg_function():

    def incr(i: int):
        return i + 1

    i = fun.Map(incr)

    assert i(41)()[41] == 42

    # Check we can call multiple times:
    r = copy.deepcopy(i(42))
    # try calling all at once
    s = copy.deepcopy(i(42, 43))

    assert s == r  # (same map, same number of calls)
    r = copy.deepcopy(r(43))
    # Note how keeping same object and mutate it, should be explicit via A = A(changes)
    # This goes against python basic syntax...

    assert r > s  # (same map, more calls - more complex)

    r()  # application
    assert r != s  # since r was applied once more (more resource intensive)
    assert r > s   # number of apply is more important than number of call.

    s()
    assert r == s

    # result are same, differs only in control flow (call/return)
    assert r[41] == s[41] == i(41) == 42
    assert r[42] == s[42] == i(42) == 43
    assert r[43] == s[43] == i(43) == 44

    s()

    # Check it will raise when no result is expected immediately (fapply underflow)
    with pytest.raises(StopIteration):
        i()

    # Check it will raise when too much call without consumption (fapply overflow)
    with pytest.raises():
        i(1)(2)(3)(4)(5)(6)(7)(8)(9)(0)


    assert i(41)(40) == 4


def test_2arg_function():
    def incr(a: int, b:int):
        return a + b
    #
    # i = fun.G(incr)
    #
    # assert callable(i)
    # assert callable(i(41))
    #
    # # Check result is in the iterator
    # assert next(i(41)) == 42
    # # check result is retrievable by unit apply
    # assert i(41)() == 42
    #
    # # Check it will raise when no result is expected immediately (fapply underflow)
    # with pytest.raises(StopIteration):
    #     i()
    #
    # # Check it will raise when too much call without consumption (fapply overflow)
    # with pytest.raises():
    #     i(1)(2)(3)(4)(5)(6)(7)(8)(9)(0)



if __name__ == '__main__':
    pytest.main(['-s', __file__])