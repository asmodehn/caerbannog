#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations


import contextlib
import math

import functools
import turtle
import enum
import typing

import pint

ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1




# nametuple because it is portable, well known, and simple to use. However see http://www.attrs.org/en/stable/why.html#namedtuples
# LATER : dataclasses, or frozen attrs.
class TurtleState(typing.NamedTuple):
    """
    Immutable public State.
    """
    position: turtle.Vec2D = turtle.Vec2D(0, 0)
    angle: int = 1 * ureg.degrees  # pint and types ???
    pen: PenState = PenState.DOWN



class TurtleImpl(typing.NamedTuple):
    """
    Basic class to hold implementation and state together
    For simplicity sake
    """
    state: TurtleState  # Note : if this was a data class we could code here the state extraction from impl.
    impl: turtle.Turtle



# Ref : https://vimeo.com/162054542

def schoenfinkel(fun):
    """
    Curry the function : changes some parameters (the ones not passed at first) into a later function call.
    Effectively splits one call into two.
    >>> def add(a,b):
    ...    return a + b
    >>> addfirst = curry(add)
    >>> andthen = addfirst(2)
    >>> addthen(3)
    5
    """
    def curried(*args, **kwargs):
        # TODO : check type signature vs traditional function (haskell and others)
        p = functools.partial(fun, *args, **kwargs)

        return p

    return curried

# TODO : there is probably a more straightforward way fo defining curry from a functools decorator function
curry = schoenfinkel


def uncurry(fun):
    """
    Uncurry the function : changes some
    :param fun:
    :return:
    """
    raise NotImplementedError # TODO


class MonadicTurtle:

    class Lifted:

        def __init__(self, f):
            self.f = f

        def __call__(self, *args, **kwargs):

            # Note : we define a lifted function for clarity,
            # but actually python parametric polymorphism is enough to do the job.
            return self.f(*args, **kwargs)

    def __init__(self, arg: TurtleImpl):  # Note : this is the Type we pass (to start designing monad in a generic way)
        self.arg = arg

    def __call__(self, fun) -> MonadicTurtle.Lifted:
        """
        Decorator to mark a function as a generator of M_argtype ie. M_T
        :param arg:
        :return:
        """

        # TODO : assert fun is of the right type : one input  only, and one output of paramter type of T

        # TODO : test if function is not partial and has more than one arg -> curry it

        # TODO : ensure function has this arg, and return it, and generate monad class from it

        return MonadicTurtle.Lifted(curry(fun))



@contextlib.contextmanager
def montle() -> TurtleImpl:
    """ A context in which a turtle is available, as well as its state"""
    ft = turtle.Turtle()
    yield TurtleImpl(impl=ft, state=TurtleState(position=ft.position(), angle=ft.heading(), pen=ft.pen().get('pendown')))
    # TODO : exit cleanly


@MonadicTurtle('impl')
def move(distance: int, impl: TurtleImpl):

    # TMP HACK
    distance = int(distance)

    # precomputing movable distance to remain in screen
    # TODO : convert screen coord / worldcoords
    TL, BL, BR, TR = map(lambda x: turtle.Vec2D(*(impl.impl.screen.screensize()[0] * x[0] * 0.5, impl.impl.screen.screensize()[1] * x[1] * 0.5)),
                                                [(-1, 1), (-1, -1),(1,-1),(1,1)])
    # forecasting position (TODO : test code)
    forecast_pos = impl.state.position + (turtle.Vec2D(math.cos(impl.state.angle), math.sin(impl.state.angle)) * distance)
    #impl.impl.forward(distance)
    #assert impl.impl.position() == forecast_pos, f"{impl.impl.position()} is not {forecast_pos}"

    # capping distance (implementing artificial canvas limitations):
    capped_distance = distance
    if forecast_pos[0] > (BR + TR)[0] or forecast_pos[1] > (TL + TR)[1]:
        forecast_pos = ( min( (BR + TR)[0], forecast_pos[0]), min((TL + TR)[1], forecast_pos[1]))
    if forecast_pos[0] < (BL + TL)[0] or forecast_pos[1] < (BL + BR)[1]:
        forecast_pos = (max((BL +TL)[0], forecast_pos[0]), max((BL+BR)[1], forecast_pos[1]))

    capped_distance = math.sqrt( math.pow(forecast_pos[0] - impl.state.position[0],2) + math.pow(forecast_pos[1] - impl.state.position[1], 2))
    impl.impl.forward(capped_distance)

    # moved distance ...
    # It's the opposite of what we coull be doing here for control...
    # delta = deltapos(expected_reached, reached_pos) and return delta to adjust next call...
    # Note :  TODO : because of this 04 seems to be a good place to introduce control instead of 3...
    # TODO : however it is probably better to wait until we get events to log out control and be able to debug/replay it.
    # TODO : OR NOT ? do we have a way to gradually optimise higher control, ie log of control ? That is, the more it works, the less we want to log about it.


    # return new state (it is immutable)
    return TurtleImpl(impl=impl.impl, state=TurtleState(position=impl.impl.position(), angle=impl.impl.heading(), pen=impl.impl.pen().get('pendown'))), capped_distance


@MonadicTurtle('impl')
def right(angle: int, impl: TurtleImpl):

    # TMP HACK
    angle = int(angle * ureg.degrees)

    impl.impl.right(angle)

    # return new state (it is immutable)
    return TurtleImpl(impl=impl.impl, state=TurtleState(position=impl.impl.position(), angle=impl.impl.heading(), pen=impl.impl.pen().get('pendown')))


@MonadicTurtle('impl')
def left(angle: int, impl: TurtleImpl):

    # TMP HACK
    angle = int(angle)

    impl.impl.left(angle)

    # return new state (it is immutable)
    return TurtleImpl(impl=impl.impl, state=TurtleState(position=impl.impl.position(), angle=impl.impl.heading(), pen=impl.impl.pen().get('pendown')))


@MonadicTurtle('impl')
def penup(impl: TurtleImpl):
    impl.impl.penup()

    # return new state (it is immutable)
    return TurtleImpl(impl=impl.impl, state=TurtleState(position=impl.impl.position(), angle=impl.impl.heading(), pen=impl.impl.pen().get('pendown')))


@MonadicTurtle('impl')
def pendown(impl: TurtleImpl):
    impl.impl.pendown()

    # return new state (it is immutable)
    return  TurtleImpl(impl=impl.impl, state=TurtleState(position=impl.impl.position(), angle=impl.impl.heading(), pen=impl.impl.pen().get('pendown')))



