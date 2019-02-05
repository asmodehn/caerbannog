import turtle


import enum
import pint
ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# The usual OO inheritance interface
# taking turtle.Turtle as an unknown black box.
# We just provide shortcuts to some of its methods and attributes here for clarity.
class Turtle(turtle.Turtle):

    @property
    def position(self):
        return super().position

    @property
    def angle(self):
        return super().heading()

    @property
    def penState(self):
        return super().pen().get('pendown')

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        super().forward(distance=distance)

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle * ureg.degrees)

        super().right(angle)

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        super().left(angle)

    def penup(self):
        super().penup()

    def pendown(self):
        super().pendown()
