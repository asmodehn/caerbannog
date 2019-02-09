import turtle


import enum
import pint
ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# Using class as data structure, for typing, and '_' as the usual python convention for "private".
# Remember, Types were used before Object Oriented programming...
# The usual OO delegation interface
# taking turtle.Turtle as an unknown black box.
# Composition, not inheritance.
class _TurtleState:

    @property
    def position(self):
        return self.mutate.position  # TODO : mutable

    @property
    def angle(self):
        return self.mutate.heading()  # TODO : mutable

    @property
    def penState(self):
        return self.mutate.pen().get('pendown') # TODO mutable

    def __init__(self, real_turtle: turtle.Turtle):
        # one attribute as interface and entry point for mutation
        self.mutate = real_turtle


def create():
    return _TurtleState(turtle.Turtle())


def move(distance: int, state: _TurtleState):

    # TMP HACK
    distance = int(distance)

    # This will mutate the state
    state.mutate.forward(distance=distance)


def right(angle: int, state: _TurtleState):

    # TMP HACK
    angle = int(angle * ureg.degrees)

    # This will mutate the state
    state.mutate.right(angle)


def left(angle: int, state: _TurtleState):

    # TMP HACK
    angle = int(angle)

    # This will mutate the state
    state.mutate.left(angle)


def penup(state: _TurtleState):
    state.mutate.penup()


def pendown(state: _TurtleState):
    state.mutate.pendown()





