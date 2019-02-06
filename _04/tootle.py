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
        self.real = turtle.Turtle()

    def __enter__(self):

        def do(func, arg):
            return func(arg, self)[1]

        return do

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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



def move(distance: int, state: TurtleState):

    # TMP HACK
    distance = int(distance)

    state.move(distance=distance)
    distdiff = 42

    return state, distdiff


def right(angle: int, state: TurtleState):

    # TMP HACK
    angle = int(angle * ureg.degrees)

    state.right(angle)

    return state


def left(angle: int, state: TurtleState):

    # TMP HACK
    angle = int(angle)

    state.left(angle)

    return state


def penup(state: TurtleState):
    state.penup()

    return state


def pendown(state: TurtleState):
    state.pendown()

    return state


