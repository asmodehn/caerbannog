import copy
import itertools

import functools

import typing
import queue
from dataclasses import dataclass, field

"""

Here we emulate a very basic computer model with queues and stacks...
"""

#TODO : simplified version with basic copyable containers, like list.

T = typing.TypeVar('T')

# TODO : stack of queues, or queue of stacks ? maybe there is some kind of duality here ??
# Some relation with Category Theory's natural transformation composition (vertical / horizontal) ?


# TODO : check for some interpretation in Interactive CombinaAtors (since we have linearity of message in queues)

@dataclass(init=False, frozen = True)
class A:
    """
    CAREFUL while debugging this.
    Debugging an iterator breaks its linearity (information must be duplicated to not break it).
    """
    args : typing.Iterable[typing.Any]  # TODO maybe lock on the input type of the function?
    kwargs : typing.Mapping[str, typing.Any]
    # TODO : ensure serializable... HOW ? send code around ?
    _argit : typing.Optional[typing.Iterator] = field(init=False, repr=False)

    @property
    def is_live(self):
        return self._argit is not None

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, 'args', args)
        object.__setattr__(self, 'kwargs', kwargs)
        object.__setattr__(self, '_argit', self.args.__iter__())

    def __iter__(self):
        return self

    def __next__(self):  # Iterator over arguments
        if self._argit is None:  # dead self
            raise StopIteration
        try:
            if self.kwargs:
                return next(self._argit), self.kwargs
            else:
                return next(self._argit)
        except StopIteration:
            # Self just died
            object.__setattr__(self, '_argit', None)
            raise StopIteration

    def __call__(self, *args, **kwargs):  # apply Identity

        # merging the decorations
        kwargs = {**self.kwargs, **kwargs}

        if self._argit:
            # Teeing iterators and tricking immutability...
            first, secnd = itertools.tee(self._argit)
            object.__setattr__(self, '_argit', first)

            # Immutability helps a lot here to avoid unexpected resurrection (aka zombies)
            return A(*itertools.chain(secnd, args), **kwargs)  # CAREFUL : applying args as args, and kwargs as kwargs
        else:
            return A(*args, **kwargs)  # CAREFUL : applying args as args, and kwargs as kwargs

@dataclass
class IQ:
    """
    An iterator on a queue
    """
    q: queue.Queue = field(default_factory=functools.partial(queue.Queue, maxsize=32))

    def __iter__(self):
        # Handling underflow
        def  sentinel():
            pass
        return iter(self.q, sentinel)


    def __call__(self, *args: typing.Any, **kwargs: typing.Any):
        # Handling overflow
        self.q.put_nowait(A(args=args, kwargs=kwargs))


@dataclass
class MQ:
    """
    An iterator on a stack of queues
    """
    qstack: typing.Optional[queue.LifoQueue] = field(default = None)
    current: queue.Queue = field(default_factory=functools.partial(IQ))

    def __iter__(self):
        def  sentinel():
            pass
        return iter(self.qstack, sentinel)


def fork(q: MQ):  # Categorically : MQ product ? MQ sum ? other ?

    qq = MQ(qstack=queue.LifoQueue(maxsize=8))
    mq = MQ(qstack=queue.LifoQueue(maxsize=8))

    # duplicating data will take time...
    # TODO : better way ? SIC ?
    for m in q:
        mm = copy.deepcopy(m)  # Note we need a deep copy, that guarantees equality of duplicates
        qq.qstack.put(m)
        mq.qstack.put(mm)

    return qq, mq


def join(q1:MQ, q2:MQ ):

    mq = MQ(qstack=queue.LifoQueue(maxsize=8))

    for m1 in q1:
        for m2 in q2:
            if m1 == m2:
                mq.current.put(m1)

    return mq




def queue(stackmax):

    class QueueGroup:

        def __init__(self, callqueue=32):
            """Build a limited queue of max size 256.
            Overall memory usage will depend on what is inside, but queue must be limited,
             mainly as a way to enforce code simplicity.
            """
            self.callqueue = 32
            self.current = queue.Queue()
            self.stack = queue.LifoQueue(maxsize=stackmax)  # We keep historical queues in a stack

        def put(self, item: T, block: bool = True, timeout: typing.Optional[float] = None):
            return self.current.put(item, block=block, timeout=timeout)

        def get(self, block: bool = True, timeout: typing.Optional[float] = None) -> T:
            return self.current.get(block=block, timeout=timeout)

        def split(self):
            self.stack.put(self.current)
            self.current = queue.Queue

            return QueueGroup()


        def join(self):
            pass

    return QueueGroup

