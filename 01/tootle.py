import turtle

import enum

import pint
ureg = pint.UnitRegistry()


# We use enum for simple values as type
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# The usual OO inheritance interface
# taking turtle.Turtle as an unknown black box.
# We provide shortcuts to some of its methods and attributes here for interfacing with turtle,
# while trying to keep the turtle API small.
class Tootle(turtle.Turtle):
    """
    Inheriting from provided Turtle class, OO style.
    >>> t = Tootle()


    """
    @property
    def position(self):
        return super().position() * ureg.pixel

    @property
    def angle(self):
        return super().heading() * ureg.degrees

    @property
    def penState(self):
        return super().pen().get('pendown')

    def move(self, distance: int):
        super().forward(distance=distance)

    def right(self, angle: int):
        super().right(angle * ureg.degrees)

    def left(self, angle: int):
        super().left(angle * ureg.degrees)

    def penup(self):
        super().penup()

    def pendown(self):
        super().pendown()
