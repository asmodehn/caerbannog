import unittest

from hypothesis import given, infer
from hypothesis import strategies as st

from fun.immutable.looperset import looperset, TypeSet


class TestLooperSet(unittest.TestCase):
    """ Testing LooperSet - should be a bimonad in time and state in python """

    def test_empty_falsy(self):
        assert bool(looperset()) == False

    # TODO : test usual / expected set behavior

    @given(st.data())
    def test_monad_int(self,  data):
        """ Testing monadic interface on DList[int] """

        t = data.draw(st.integers())
        ls = looperset(t, t)   # monadic return

        assert isinstance(ls, TypeSet)
        assert t in ls   # we can check the contents  !  # TODO : on type instead ??

        # monadic return on instance, in time-dimension, via __call__ to make it similar to the type constructor.
        dlbis = ls(t)
        assert dlbis == looperset(t, t, t)

        # implicit monadic join
        lls = looperset(looperset(t, t))

        assert lls == ls

        # CAREFUL !
        llls = looperset(looperset(t), looperset(t))

        assert llls != ls

    @given(st.data())
    def test_comonad_int(self, data):
        """ Testing comonadic interface on DList[int] """

        t = data.draw(st.integers())
        ls = looperset(t, t)  # monadic return

        assert isinstance(ls, TypeSet)
        assert t in ls  # we can check the contents  !  # TODO : on type instead ??

        # next as getting subtype , via the comonadic extract in TIME.
        # It is not the one in STATE - getitem - and uses different types because of container time semantics.
        assert next(ls) == looperset(t)
        assert next(ls) == looperset(t)
        # we can go on for ever but
        assert next(next(ls)) == looperset
        # Note : there is a (affine ?) time semantic of cunsomption here in one line, but not in sequential call...

        # CAREFUL with monadic join, it doesnt alter structure !
        llls = looperset(looperset(t), looperset(t))
        assert llls != ls

        lllsn = next(llls)
        assert lllsn != t
        assert lllsn == looperset(t)

    # TODO : algebra


if __name__ == '__main__':
    unittest.main()