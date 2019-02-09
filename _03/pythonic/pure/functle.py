import turtle
import enum
import pint
ureg = pint.UnitRegistry()

import purity

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

    # underscored to prevent overriding when pipelining...
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


# Class as owner of the state, used for composing turtle functions
class Functle:

    def __init__(self):
        self.state = TurtleState()

    def move(self, distance: int):
        # TMP HACK
        distance = int(distance)

        self.state.move(distance=distance)

        return self

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle * ureg.degrees)

        self.state.right(angle)

        return self

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        self.state.left(angle)

        return self

    def penup(self):
        self.state.penup()

        return self

    def pendown(self):
        self.state.pendown()

        return self



