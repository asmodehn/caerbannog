import turtle
import enum
import pint

ureg = pint.UnitRegistry()


# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# Simplest interface for clarity, but can only support one turtle.
# We use this global as a way to simplify functions interface to keep clarity.
_abstle = None


# Using class as data structure, for typing, and '_' as the usual python convention for "private".
# Remember, Types were used before Object Oriented programming...
# The usual OO delegation interface
# taking turtle.Turtle as an unknown black box.
# Composition, not inheritance.
class _TurtleState:
    """
    TurtleState is mutable and therefore private.
    """

    def __init__(self):
        self.update()

    def update(self):
        global _abstle

        """Update from the global abstle"""
        self.position = _abstle.position()
        self.angle = _abstle.heading()
        self.penState = _abstle.pen().get("pendown")


def create(supermodel=None):
    global _abstle
    _abstle = supermodel if supermodel is not None else turtle.Turtle()
    return _TurtleState()


def move(distance: int, state: _TurtleState):
    global _abstle

    # TMP HACK
    distance = int(distance)

    _abstle.forward(distance=distance)

    # This will mutate the state
    state.update()


def right(angle: int, state: _TurtleState):
    global _abstle

    # TMP HACK
    angle = int(angle * ureg.degrees)

    _abstle.right(angle)

    # This will mutate the state
    state.update()


def left(angle: int, state: _TurtleState):
    global _abstle

    # TMP HACK
    angle = int(angle)

    _abstle.left(angle)

    # This will mutate the state
    state.update()


def penup(state: _TurtleState):
    global _abstle
    _abstle.penup()
    # This will mutate the state
    state.update()


def pendown(state: _TurtleState):
    global _abstle
    _abstle.pendown()
    # This will mutate the state
    state.update()
