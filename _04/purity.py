import unittest

import functools
import inspect

"""
A single drag'n'drop module to purify your python.
AKA The Rabbit of Caerbannog.
"""

class Impure(RuntimeWarning):
    pass


_registry = dict()


# Function, in the proper sense
class Pure:
    """
    Class implementing purity check, wrapping usual python function to enforce and certify its purity.
    We use a class to be able to use type checks to differentiate with usual, potentially impure, python functions.
    >>> def add42(x):
    ...   return x + 42
    >>> p = Pure(add42)

    An instance is callable just like any other function
    >>> p(8)
    50

    Composition of pure functions is implemented as attribute access...
    >>> p.p(16)
    100

    Purity will be verified at runtime (leveraging memoization).
    >>> glob = True
    >>> def add42_impure(y):
    ...   global glob
    ...   if glob:
    ...     glob = False
    ...     return y + 42
    ...   else:
    ...     return y + 41

    >>> i = Pure(add42_impure)
    >>> i(8)
    50

    >>> i(8)
    Traceback (most recent call last):
    ...
    purity.Impure


    Multiple calls are memoized
    >>> import hashlib
    >>> def sha256(str):
    ...   for i in range(2000):  # many times to get measurable performance improvement
    ...     hash_object = hashlib.sha256(b'Hello World')
    ...   return hash_object.hexdigest()
    >>> s = Pure(sha256)
    >>> import time
    >>> start = time.clock(); s("Caerbannog"); lap = time.clock() - start; print(lap)  # doctest: +ELLIPSIS
    'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
    ...
    >>> start = time.clock(); s("Caerbannog"); lap = time.clock() - start; print(lap)  # doctest: +ELLIPSIS
    'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
    ...
    >>> start = time.clock(); s("Caerbannog"); lap = time.clock() - start; print(lap)  # doctest: +ELLIPSIS
    'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
    ...

    TODO : but not if memory query would be slower...
    """

    def __init__(self, func):
        self.f = func
        self.__name__ = func.__name__  # TODO : proper clean wrapper https://hynek.me/articles/decorators/
        self.sig = inspect.signature(func)
        _registry[func.__name__] = self
        self.memo = dict()  # TODO : hard limit on memory usage (evolving)

        self.calls = 0
        self.check_period = 1  # every n calls

    def __call__(self, *args, **kwargs):
        # args must be hashable
        bound_args = self.sig.bind(*args, **kwargs)

        # first time : store call result
        if bound_args.args not in self.memo:
            self.memo[bound_args.args] = self.f(*bound_args.args)
        elif self.calls % self.check_period == 0:
            # if it s time for a checkup
            result = self.f(*bound_args.args)
            if result != self.memo[bound_args.args]:
                # reset check_period
                self.check_period = 1
                raise Impure
            else:
                # increase check period exponentially
                # TODO : studies needed for optimal performance here...
                self.check_period *= 2

        # increase call number
        self.calls += 1
        # return stored result
        return self.memo[bound_args.args]

    def __getattr__(self, item):
        # access calling context
        callframe = inspect.getouterframes(inspect.currentframe())[1]
        # resolving item
        item = callframe.frame.f_locals.get(item)

        assert type(item) is Pure
        if item.__name__ in _registry:
            g = _registry.get(item.__name__)
            def composed(*args, **kwargs):
                return self(g(*args, **kwargs))
            return composed
        else:
            raise NotImplementedError(item)


class TestPure(unittest.TestCase):

    def test_pure(self):
        pass

    def test_impure(self):
        pass

    def test_memoize(self):
        pass

    def test_compose(self):
        pass

# TODO : class for benchmark
# https://www.peterbe.com/plog/how-to-do-performance-micro-benchmarks-in-python
class BenchPure():
    pass


def pure(func):
    """
    Decorator for Pure
    """
    p = Pure(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    # TODO : simplest repl for module self test...
    import random
    import time

    @pure
    def add42_pure(x):
        return x + 42

    @pure
    def add4x_impure(y):
        return y + 42 + random.randint(1, 2)

    # test purity
    p = Pure(add42_pure)

    start = time.time()
    for v in range(2000):
        p(v)
    lap = time.time() - start

    print(f"pure calls took {lap} seconds")

    for v in range(2000):
        p(v)
    finish = time.time() - lap
    print(f"pure memoized calls took {finish} seconds")

    # test impurity
    i = Pure(add4x_impure)

    start = time.time()
    for w in range(2000):
        i(w)
    lap = time.time() - start

    print(f"impure calls took {lap} seconds")

    for w in range(2000):
        i(w)
    finish = time.time() - lap
    print(f"impure memoized calls took {finish} seconds")

