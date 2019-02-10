import pickle
import turtle
import enum
import pint
import typing
ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# nametuple because it is portable, well known, and simple to use. However see http://www.attrs.org/en/stable/why.html#namedtuples
# LATER : dataclasses, or frozen attrs.
class TurtleState(typing.NamedTuple):
    """
    Immutable public State
    """
    position: turtle.Vec2D = turtle.Vec2D(0, 0)
    angle: int = 1 * ureg.degrees  # pint and types ???
    pen: PenState = PenState.DOWN


# Class as owner/wrapper of the state, used for composing turtle functions.
# We can use the state as representation of our instance, since there are only pure functions here.
class Functle:

    @property
    def state(self):
        return TurtleState(self.real.position(), self.real.heading(), self.real.pen().get('pendown'))

    def __repr__(self):
        return repr(self.state)

    def __init__(self):
        self.real = turtle.Tootle()

    def move(self, distance: int):
        # TMP HACK
        distance = int(distance)

        self.real.forward(distance=distance)

        return self

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle * ureg.degrees)

        self.real.right(angle)

        return self

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        self.real.left(angle)

        return self

    def penup(self):
        self.real.penup()

        return self

    def pendown(self):
        self.real.pendown()

        return self



