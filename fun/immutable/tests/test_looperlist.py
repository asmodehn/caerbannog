import unittest

from hypothesis import given, infer
from hypothesis import strategies as st

from immutable.looperlist import looperlist, LooperList, EmptyLooperList


class TestDListTime(unittest.TestCase):
    """ DList is a time(call/next) - BiMonad in python  - and a usual list in the usual state dimension"""

    def test_empty_falsy(self):
        assert bool(looperlist()) == False

    # TODO : test usual / expected list behavior

    @given(st.data())
    def test_monad_int(self,  data):
        """ Testing monadic interface on DList[int] """

        t = data.draw(st.integers())
        dl = looperlist(t, t)   # monadic return

        assert isinstance(dl, LooperList)
        assert t in dl   # we can check the contents  !  # TODO : on type instead ??

        # monadic return on instance, in time-dimension, via __call__ to make it similar to the type constructor.
        dlbis = dl(t)
        assert dlbis == looperlist(t, t, t)

        # implicit monadic join
        ddl = looperlist(looperlist(t, t))

        assert ddl == dl

        # CAREFUL !
        dld = looperlist(looperlist(t), looperlist(t))

        assert dld != dl

    @given(st.data())
    def test_comonad_int(self, data):
        """ Testing comonadic interface on DList[int] """

        t = data.draw(st.integers())
        dl = looperlist(t, t)  # monadic return

        assert isinstance(dl, LooperList)
        assert t in dl  # we can check the contents  !  # TODO : on type instead ??

        # next as getting subtype , via the comonadic extract in TIME.
        # It is not the one in STATE - getitem - and uses different types because of container time semantics.
        assert next(dl) == looperlist(t)
        assert next(dl) == looperlist(t)
        # we can go on for ever but
        assert next(next(dl)) == EmptyLooperList
        # Note : there is a (affine ?) time semantic of cunsomption here in one line, but not in sequential call...

        # CAREFUL with monadic join, it doesnt alter structure !
        dld = looperlist(looperlist(t), looperlist(t))
        assert dld != dl

        dln = next(dld)
        assert dln != t
        assert dln == looperlist(t)
