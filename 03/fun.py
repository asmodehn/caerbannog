#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import contextlib
import copy
import inspect
import queue
import app
import collections

import functools
import turtle
import enum
import typing

# We want a clean functional python code, even though python is not made for this...
# => Efficiency will be secondary to clarity.
# Note : Terseness is another thing altogether and is a non-goal,
# because the final aim is to generate code on the fly.
# => Highest Priority : Code Semantic Clarity (given Category Theory and Map Theory knowledge).


#TODO : single dispatch on first argument (th only one in our design...)

class Map(collections.OrderedDict):
    """
    Callable Iterator as a curried function with iterable arguments, supporting multi call sequence.
    Allows decoupling calling a function and receiving a result, while keeping most of python function call capabilities.
    BEWARE: Map is mutable, so that future computation is not done again if it was already done in the past.
    """

    def __init__(self, f, existing=None):
        # TODO : maxsize + overflow/underflow exceptions
        self._calls = app.QueueGroup()  # TODO: call queue or call stack ??
        self._inner = f
        super().__init__(existing or {})

    def __next__(self):
        """
        Iterator has a different meaning here : We want result of next() application
        :return:
        """
        if not callable(self._inner):
            return self._inner
        elif not inspect.signature(self._inner).parameters:
            return self._inner()  # no need to wait for call before getting result.
        else:
            # retrieve call from queue (apply by need)
            # But one at a time
            needed = self._calls.get_nowait()
            for a in needed:
                assert callable(needed[a])
                self[a] = needed[a]()  # TODO: What if over max dict size ?
            self._calls.task_done()

        return self

    def __lt__(self, other):
        """
        One Map is less than another iff one map is less than another, or number of calls is less than another.
        CHecking in that order is important, the presence in the map means more actuation has been done.
        :param other:
        :return:
        """
        return super().__lt__(other) or self._calls.unfinished_tasks < other._calls.unfinished_tasks

    def __eq__(self, other):
        """
        Strict equality : must be same mapping content, same queued calls.
        Note the intrinsic equality of function is a matter of implementation and should not matter at this level (Yoneda Lemma)
        :param other:
        :return:
        """
        return super().__eq__(other) and self._calls.unfinished_tasks == other._calls.unfinished_tasks  # and self._inner == other._inner

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __repr__(self):
        """Consistent repr"""
        return super().__repr__() + self._calls.__repr__()

    def __call__(self, *args, **kwargs):
        # Note if args are sequential 1-arg calls, kwargs are onetime n-arg calls.
        # => enforce unambiguous coding style when user wants to bypass functional iterative call implementation.

        if args or kwargs:

            if callable(self._inner) and inspect.signature(self._inner).parameters:
                # Iterate on arguments and construct a mapping, for later application
                self._calls.put_nowait(
                    {a: functools.partial(self._inner, a, **kwargs) for a in args if a not in self}
                )  # TODO : what if over max queue size ?
                return self  # for successive curried application
            else:
                # silently absorb useless args.
                return self  # for successive curried application

        else:
            # TODO : do we do it here, or in the 'background' (potentially another thread later), or on demand?
            return next(self)  # empty call marks one application and retrieval of result.

    def __copy__(self):
        """
        When duplicating the Map, the Map itself must remain the same (_inner is assumed a pure function)
        However the call queue must be different as to not have the same Map for ever, resource-wise...
        Note this goes against python core functionality, so implementing an Interactive Combinator based paradigm will not look pretty...
        Maybe in a specific context (with:) ?

        TODO What is the meaning of a shallow copy in this context ?
        :return:
        """

        # we do not want to keep the same reference on the super class map, only the existing content
        other = Map(self._inner, existing=self)
        # other._calls = self._calls  # drop current call queue.
        return other

    def __deepcopy__(self, memo=None):
        """
        When duplicating the Map, the Map itself must remain the same (_inner is assumed a pure function)
        However the call queue must be different as to not have the same Map for ever, resource-wise...
        Note this goes against python core functionality, so implementing an Interactive Combinator based paradigm will not look pretty...
        Maybe in a specific context (with:) ?
        :return:
        """

        # we do not want to keep the same reference on the super class map, only the existing content
        other = Map(self._inner, existing=self)  # TODO : since we copy here the function, using a memoized function should work all the same.
        # keep existing calls
        other._calls = self._calls.split()
        return other

    def __add__(self, other):
        """
        We can add maps: merging the map if _inner is the exact same, and puting one queue into another (non commutative)
        This gives as a basic lattice of maps (for the same function), by allowing joins (with the copy as meets)...
        :param other:
        :return:
        """
        pass  # TODO


if __name__ == '__main__':
    import doctest
    doctest.testmod()





