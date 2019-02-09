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
class Abstle:
    """
    Pythonic data structure : methods for mutating internal state
    """
    @property
    def position(self):
        return self.mutate.position  # TODO : mutable

    @property
    def angle(self):
        return self.mutate.heading()  # TODO : mutable

    @property
    def penState(self):
        return self.mutate.pen().get('pendown')  # TODO mutable

    def __init__(self, real_turtle: turtle.Turtle):
        # one attribute as interface and entry point for mutation
        self.mutate = turtle.Turtle()

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        # This will mutate the state
        self.mutate.forward(distance=distance)

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle * ureg.degrees)

        # This will mutate the state
        self.mutate.right(angle)

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        # This will mutate the state
        self.mutate.left(angle)

    def penup(self):
        self.mutate.penup()

    def pendown(self):
        self.mutate.pendown()





