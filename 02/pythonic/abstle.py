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
    Pythonic data structure : methods for mutating internal state.

    From a pythonic point of view, it still makes sense to have both data encaspulated in a class
    and behavior as methods of this class.

    Passing self everywhere around is effectively the same as passing the state, with more "pythonic" semantics.
    Therefore we can also use this class as interface with turtle
    """
    @property
    def position(self):
        return self.mutate.position()

    @property
    def angle(self):
        return self.mutate.heading()

    @property
    def penState(self):
        return self.mutate.pen().get('pendown')

    def __init__(self, mutable=None):
        # one attribute as interface and entry point for mutation
        self.mutate = mutable if mutable is not None else turtle.Turtle()

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





