import inspect

import types

import functools
import turtle


import enum
import pint
ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# The usual OO delegation interface
# taking turtle.Turtle as an unknown black box.
# Composition, not inheritance.
# The state is also used here as the interface to the python turtle implementation.
class TurtleState:
    @property
    def position(self) -> int:
        return self.real.position()

    @property
    def angle(self) -> int:
        return self.real.heading()

    @property
    def penState(self) -> PenState:
        return self.real.pen().get('pendown')

    def __init__(self):
        self.real = turtle.Tootle()

    def move(self, distance: int):
        self.real.forward(distance=distance)

    def right(self, angle: int):
        self.real.right(angle)

    def left(self, angle: int):
        self.real.left(angle)

    def penup(self):
        self.real.penup()

    def pendown(self):
        self.real.pendown()



# metaclass as type class
# https://en.wikibooks.org/wiki/Haskell/The_Functor_class
class Functor:

    # https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
    @classmethod
    def __prepare__(mcs, name, bases):
        pass

    def __call__(self, *args, **kwargs):
        pass

    #: fmap :: (a -> b) -> f a -> f b
    def fmap(self, pure):
        raise NotImplementedError

    def test_id(self):
        pass

    def test_composition(self):
        pass



class Applicative(Functor):

    #: pure :: a -> f a
    def pure(self):
        pass

    #: (<*>) :: f (a -> b) -> f a -> f b
    def apply(self):
        pass

    # pure id <*> v = v              -- Identity
    def test_identity(self):
        pass

    # pure f <*> pure x = pure (f x)        -- Homomorphism
    def test_homomorphism(self):
        pass

    # u <*> pure y = pure ($ y) <*> u       -- Interchange
    def test_interchange(self):
        pass

    # pure (.) <*> u <*> v <*> w = u <*> (v <*> w) -- Composition
    def test_composition(self):
        pass

    # fmap f x = pure f <*> x           -- fmap
    def test_fmap(self):
        pass


class Monad:

    def constructor(self):
        pass

    #: return :: a -> m a
    def _return(self):
        return lambda x: x

    #: (>>=)  :: m a -> (a -> m b) -> m b
    def _bind(self):
        pass


    #: m >>= return     =  m                        -- right unit
    def test_unit_right(self):
       pass

    #: return x >>= f   =  f x                      -- left unit
    def test_unit_left(self):
        pass

    #: (m >>= f) >>= g  =  m >>= (\x -> f x >>= g)  -- associativity
    def test_associativity(self):
        pass



class State:   # (functools) ?

    def __init__(self, distance):
        # TODO assert type early to avoid headache while debugging.
        self.partial = functools.partial(TurtleState.move, distance=distance)

    def __call__(self, *args, **kwargs):
        self.value, val = self.partial(*args, **kwargs)
        return val

    def __enter__(self):
        # We do not want to apply here.
        # Instead we prepare for introspection...
        # TODO
        return self.partial

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def compose(f, g):
    f(g)


class MonadicTurtle:

    # Constructor
    def __init__(self):
        # TODO : make this parameterizable somehow
        self.tstate = TurtleState()

    def __call__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def move(self, distance: int):
        # TMP HACK
        distance = int(distance)

        return functools.partial(TurtleState.move, distance=distance)


    def right(self, angle: int):
        # TMP HACK
        angle = int(angle * ureg.degrees)

        def stateFun(state: TurtleState):
            state.right(angle)

            return state

        return State(stateFun)

    def left(self, angle: int):
        # TMP HACK
        angle = int(angle)

        def stateFun(state: TurtleState):
            state.left(angle)

            return state

        return State(stateFun)

    def penup(self):
        def stateFun(state: TurtleState):
            state.penup()

            return state

        return State(stateFun)

    def pendown(self):
        def stateFun(state: TurtleState):
            state.pendown()

            return state

        return State(stateFun)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass





