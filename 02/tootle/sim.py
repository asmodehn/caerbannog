import logging
import math

from .utils import PenState
from .state import TurtleState

# Note we use a class here like "module" was used in the presentation, to encapsulate code.
# There are other ways to achieve the same goal, for example having separate module for each class used here.
class SimTurtle:

    state = TurtleState()
    #: the list of lines drawn, as the expected side effect.
    drawing = []

    # no init, just like in the code model

    # delegate attributes
    @property
    def position(self):
        return self.state.position

    @property
    def attitude(self):
        return self.state.attitude

    @property
    def penState(self):
        return self.state.penState

    # Note the state here is also passed around in self.
    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        oldpos = self.position
        self.state.move(distance)
        newpos = self.position

        # just because we manage the drawing here and not in the TurtleState
        if self.penState == PenState.DOWN:
            self.drawing.append((oldpos, newpos))

    def turn(self, angle: int):
        logging.info("simulating turn {0} degree".format(angle))

        self.state.turn(angle)

    def heading(self):
        # From https://github.com/python/cpython/blob/master/Lib/turtle.py#L1895
        return round(
            math.atan2(self.attitude[1], self.attitude[0])
            * 180.0
            / math.pi,
            10,
        ) % 360.0

    def penup(self):
        logging.info("simulating pen UP")
        self.state.penup()

    def pendown(self):
        logging.info("simulating pen DOWN")
        self.state.pendown()

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self.state.home()

    # No bye, no deletion, python garbage collect...

