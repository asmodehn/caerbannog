import functools

# TODO : we currently define it for only one argument.
# This can be extended to iterate on that argument, and be linked with itertools and others...

class ImpureFunction(Exception):
    pass

"""
Optimization of a pure function for
- runtime time (CPU time spent)
- runtime space (as memory space)

We cannot easily make sure in python that a function is pure (in the mathematical sense, without side-effects)
But we can check for idempotency over time (calling it multiple times), for example by attempting to model its execution by a Mapping.
A mapping is usually used in memoization/caching strategies.

In here we reuse the standard functools.lru_cache as a 'best-effort' endeavour to make sure (python)functions are pure.
That is, that they can be modeled by a math function, giving the same result, no matter how many times one is called.
And when detectable, trigger an exception to expose the impurity.
"""


def function(check_ratio: float = 1):
    """
    Decorator for a function, to ensure that it is representable as a mathematical function.
    Check ratio is the ratio of calls_checked / total_calls
    Unchecked calls are just using memoization via a lru_cache.

    Note : the size of the lru_cache can be adjusted based on the type...

    :return:
    """

    #TODO : time constraint ?
    #control theory ?
    #implement optimization strategy...

    def deco(func):

        #TODO : determine cache size based on type
        cached = functools.lru_cache()(func)
        checked = 0

        def wrapped(arg):

            nonlocal checked, check_ratio

            prev_res = cached(arg)
            info = cached.cache_info()

            if checked < (info.misses + info.hits) * check_ratio:

                res = func(arg)
                checked += 1
                if prev_res != res:  # CAREFUL with equality (is / ==)
                    raise ImpureFunction()
            else:
                return prev_res

            #just doit
            return func(arg)

        return wrapped

    return deco

