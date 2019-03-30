import app
import pytest


def test_a_iter():
    a = app.A(1)

    # Test Birth
    assert next(a) == 1
    # Test Death
    with pytest.raises(StopIteration) as exc:
        next(a)

    assert exc.type is StopIteration


def test_a_iter_call_assign():
    a = app.A(1, 2)

    assert next(a) == 1

    b = a(3)

    # Test b Birth (iterating on duplicated remaining a elements)
    assert next(b) == 2

    # Beware Python reference semantics...
    # a is still live, and it s iterator is still in the same position
    assert next(a) == 2

    assert next(b) == 3

    # Letting b die
    with pytest.raises(StopIteration) as exc:
        next(b)

    assert exc.type is StopIteration

    # Letting a die
    with pytest.raises(StopIteration) as exc:
        next(a)

    assert exc.type is StopIteration

    # Replacing a
    a = a(3)
    assert next(a) == 3

    # Creating c from a's corpse
    c = a(4, 5)
    assert next(c) == 4
    assert next(c) == 5

    # C dies
    with pytest.raises(StopIteration) as exc:
        next(c)

    assert exc.type is StopIteration


def test_a_call_decorated_iter_call_assign():
    a = app.A(1, 2, one=True, two=True)

    assert next(a) == (1, {'one': True, 'two': True})

    b = a(3, three= True)

    # Test b Birth (note how decoration have merged. b comes from a)
    assert next(b) == (2, {'one': True, 'two': True, 'three': True})

    # Beware Python reference semantics...
    # a is still live, and its decoration are still unchanged
    assert next(a) == (2, {'one': True, 'two': True})

    assert next(b) == (3, {'one': True, 'two': True, 'three': True})

    # Letting b die
    with pytest.raises(StopIteration) as exc:
        next(b)

    assert exc.type is StopIteration

    # Letting a die
    with pytest.raises(StopIteration) as exc:
        next(a)

    assert exc.type is StopIteration

    # Replacing a
    a = a(3, three= True)
    assert next(a) == (3, {'one': True, 'two': True, 'three': True})

    # Creating c from a's corpse
    c = a(4, 5, four=True, five=True)
    assert next(c) == (4, {'one': True, 'two': True, 'three': True, 'four':True, 'five':True})
    assert next(c) == (5, {'one': True, 'two': True, 'three': True, 'four':True, 'five':True})

    # C dies
    with pytest.raises(StopIteration) as exc:
        next(c)

    assert exc.type is StopIteration


def test_iq_call_iter_inverse():  # TODO : q fixture
    q = app.IQ()

    q(1)  # TODO : test  hypothesis here...

    assert next(q) == 1


def test_iq_underflow():
    q = app.IQ()

    with pytest.raises() as exc:
        next(q)

    assert exc


def test_iq_overflow():
    q = app.IQ()

    with pytest.raises() as exc:
        for n in range(q.q.qsize):
            q(n)

    assert exc


# split and join are 'orthogonal' to put and get
# TODO : formalize that...
def test_split():

    q = app.Queue()

    # add random data
    q.put(42)


    # split queue

    qq = q.split()

    qq.put(43)

    assert q.pop() == 42
    assert q.empty()

    assert qq.pop() == 43
    assert qq.pop() == 42
    assert qq.empty()


def test_join():

    q = app.Queue()

    # add random data
    q.put(42)

    # split queue

    qq = q.split()

    qq.put(43)

    j = q + qq

    assert j.pop() == 43
    assert j.pop() == 42

    assert j.empty()


#closure, associativity, identity and invertibility
#
# def test_closure():
#     pass
#
#
# def test_associativity():
#     pass
#
#
# def test_identity():
#     pass
#
#
# def test_invertability():
#     pass






if __name__ == '__main__':
    pytest.main(['-s', __file__])