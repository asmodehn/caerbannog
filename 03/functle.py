import inspect

import typing

import functools
import turtle


import enum
import pint
ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


class Functle():
    """
    Since the state is now immutable, we need to have this class as interface with the actual turtle implementation
    """

    def __init__(self):
        self.real = turtle.Turtle()

    def getState(self):
        """
        Private convenience function to generate a State from a Turtle
        :return:
        """

        return TurtleState(position=self.real.position(), angle=self.real.heading(), pen=self.real.pen().get('pendown'))


# nametuple because it is portable, well known, and simple to use. However see http://www.attrs.org/en/stable/why.html#namedtuples
# LATER : dataclasses, or frozen attrs.
class TurtleState(typing.NamedTuple):
    """
    Immutable public State.
    """
    position: turtle.Vec2D = turtle.Vec2D(0, 0)
    angle: int = 1 * ureg.degrees  # pint and types ???
    pen: PenState = PenState.DOWN



def move(distance: int, state: TurtleState):

    # TMP HACK
    distance = int(distance)

    t = state.real
    t.forward(distance=distance)

    # return new state (as if it was immutable)
    return TurtleState(t)


def right(angle: int, state: TurtleState):

    # TMP HACK
    angle = int(angle * ureg.degrees)

    state._mutate.right(angle)

    return state


def left(angle: int, state: TurtleState):

    # TMP HACK
    angle = int(angle)

    state._mutate.left(angle)

    return state


def penup(state: TurtleState):
    state._mutate.penup()

    return state


def pendown(state: TurtleState):
    state._mutate.pendown()

    return state



