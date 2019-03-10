import inspect

#import profile  #: higher overhead and require calibration. BEtter for python debugging, and maybe better on average after calibration ?
import cProfile as profile  # better for quick results, if no debugging needed.
import pstats

# TODO : nice output eventually : https://stackoverflow.com/questions/4544784/how-can-you-get-the-call-tree-with-python-profilers
import sys

import typing
import functools
from dataclasses import dataclass, field
import time


"""
This module implements a live profiler, to take corrective action if:
 - a function is called too often
 - calls to the same function take too long overall
 - more ?
"""


# TODO : snakeViz for visualisation
@dataclass
class LiveProfile:

    profiler: profile.Profile = field(init=False, default=None, repr=False)

    func: typing.Callable = field(init=True)
    timer: typing.Callable = field(init=True, repr=False)

    ncalls: int = field(init=False, default=0)
    spent_time: float = field(init=False, default=0.0)
    cum_spent_time: float = field(init=False, default=0.0)
    callers: dict = field(init=False, default_factory=dict, repr=False)

    def __post_init__(self):
        # Note we make the choice of not exposing bias.
        self.profiler = profile.Profile(timer=self.timer)
        # if used, it should be infered from runtime...

        # Stats dict item structure (python 3.7):
        # (file, line, function_name): (ncalls, <-1>?, ?, ? , {(caller_file, caller_line, caller_name): ncalls})
        self._stats_idx = (self.func.__code__.co_filename, self.func.__code__.co_firstlineno, self.func.__code__.co_name)

        # TODO : making the profiler transparent
        # functools.wraps(self.func)(self.__call__)
        # NOT WORKING !

    def __call__(self, *args, **kwargs):
        """We replicate runcall here to be able to easily adapt for our usecase"""

        res = self.profiler.runcall(self.func, *args, **kwargs)

        # Note: we must call simulate_cmd_complete (called by create_stats), or the next dispatch will assert.
        self.profiler.create_stats()

        self.ncalls, _, self.spent_time, self.cum_spent_time, caller = self.profiler.stats.get(self._stats_idx)
        # Note : it seems callers are not available with cProfile
        self.callers.update(caller)  # Note : accumulation for the same caller is taken care of in the profiler already.

        # Beware : this erases the stats of the profiler !
        # self.profiler.print_stats()

        return res


# Design here comes from a somewhat opinionated point of view:
# Computing, in one location, is split in multiple 'processes'
# One process running, is a preorder of function calls.
# These function calls
# In one process (running on one compute resource - CPU, lambda in the cloud, etc.), one may want to check :
#   - the compute usage of a function call    # useful for performance check
#                                             # and choose between different implementations of the same function
#   - the memory usage of a function call     # useful for function purity checker
#   - the walltime usage of a function call   # should be doable right now. needed for limiter.
#   - the diskspace usage of a function call  # TODO
#   - the bandwith usage of a function call   # TODO

def compute_prof(func):
    """
    A profiler of wall-time spent on a function.
    The point is to find bottlenecks in human attention consumption,
    Note : there exists already a lot of profilers out there focusing on finding out CPU consumption bottlenecks,
    And we are NOT aiming at this.
    :param func:
    :return:
    """
    prof = LiveProfile(func, timer=time.process_time)
    return prof

# TODO : memory prof


def walltime_prof(func):
    """
    A profiler of wall-time spent on a function.
    The point is to find bottlenecks in human attention consumption,
    Note : there exists already a lot of profilers out there focusing on finding out CPU consumption bottlenecks,
    And we are NOT aiming at this.
    :param func:
    :return:
    """
    prof = LiveProfile(func, timer=time.perf_counter)
    return prof


if __name__ == '__main__':

    def times2(y):
        acc = y
        for _ in range(y):
            add1(acc)
        return acc

    def add1(x):
        return x + 1

    p = walltime_prof(times2)

    p(21)
    p(45)
    p(12)

    for c, t in p.callers.items():
        print(f"called by {c} {t} times")

    print(f"Total : called {p.ncalls}, duration {p.spent_time}, {p.cum_spent_time}")
