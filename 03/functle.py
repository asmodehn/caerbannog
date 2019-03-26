#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import contextlib
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
        #
        # TODO TODO TODO : not partial when all parameters have been passed, just apply !
        p = functools.partial(fun, *args, **kwargs)

        return p

    return curried


# TODO : there is probably a more straightforward way fo defining curry from a functools decorator function
curry = schoenfinkel


@schoenfinkel
def compose(*args):
    """A very simple composer, or "application accumulator".
    Will work only with curried functions, and is itself curried, to be able to use it freely.
    Note : This is just a Monoid, build on identity and the function application.
    >>> add2 = lambda x: (2 + x)
    >>> compose(add2) (compose(add2, add2)) (3)
    9

    """
    acc = args[-1] if args else lambda x: x  # monoid unit : the identity function
    for a in args[:-1][::-1]:  # taking args list, except last element, in inverse order.
        # if one of the function we compose is a constant, we treat it as the constant function
        # and compose with it by erasing the accumulated result.
        if not callable(a):
            acc = a
        else:
            if callable(acc):
                acc = functools.partial(a, acc)  # partial call because acc is not fully applied just yet
            else:
                acc = a(acc)
    return acc


@contextlib.contextmanager
def functle():
    """ A context in which a turtle is available, along with its state, and a functional application accumulator"""
    ft = turtle.Turtle()
    yield ft, TurtleState(position=ft.position(), angle=ft.heading(), pen=ft.pen().get('pendown'))
    # TODO : exit cleanly


# nametuple because it is portable, well known, and simple to use. However see http://www.attrs.org/en/stable/why.html#namedtuples
# LATER : dataclasses, or frozen attrs.
class TurtleState(typing.NamedTuple):
    """
    Immutable public State.
    """
    position: turtle.Vec2D = turtle.Vec2D(0, 0)
    angle: int = 1 * ureg.degrees  # pint and types ???
    pen: PenState = PenState.DOWN


def move(distance: int, impl: turtle.Turtle, state: TurtleState):

    # TMP HACK
    distance = int(distance)

    impl.forward(distance=distance)

    # return new state (it is immutable)
    return impl, TurtleState(position=impl.position(), angle=impl.heading(), pen=impl.pen().get('pendown'))


def right(angle: int, impl: turtle.Turtle, state: TurtleState):

    # TMP HACK
    angle = int(angle * ureg.degrees)

    impl.right(angle)

    # return new state (it is immutable)
    return impl, TurtleState(position=impl.position(), angle=impl.heading(), pen=impl.pen().get('pendown'))


def left(angle: int, impl: turtle.Turtle, state: TurtleState):

    # TMP HACK
    angle = int(angle)

    impl.left(angle)

    # return new state (it is immutable)
    return impl, TurtleState(position=impl.position(), angle=impl.heading(), pen=impl.pen().get('pendown'))


def penup(impl: turtle.Turtle, state: TurtleState):
    impl.penup()

    # return new state (it is immutable)
    return impl, TurtleState(position=impl.position(), angle=impl.heading(), pen=impl.pen().get('pendown'))


def pendown(impl: turtle.Turtle, state: TurtleState):
    impl.pendown()

    # return new state (it is immutable)
    return impl, TurtleState(position=impl.position(), angle=impl.heading(), pen=impl.pen().get('pendown'))



