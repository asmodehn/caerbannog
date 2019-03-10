from .state import TurtleState
from .utils import PenState

# Note we use a class here like "module" was used in the presentation, to encapsulate code.
# There are other ways to achieve the same goal, for example having separate module for each class used here.
# note that we return self here (the state), which gives us a "fluent API" design.
import logging
import math


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
    # Note : using self is how we pass the state(=instance) around in python !

    # Note : using self is how we pass the state(=instance) around in python !
    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        oldPosition = self.state.position

        self.state.move(distance)

        if self.state.penState == PenState.DOWN:
            self.drawing.append((oldPosition, self.state.position))

        return self

    def turn(self, angle: int):
        logging.info("simulating turn {0} degree".format(angle))

        self.state.turn(angle)

        return self

    def heading(self, state: TurtleState):
        # From https://github.com/python/cpython/blob/master/Lib/turtle.py#L1895
        return round(
            math.atan2(state.attitude[1], state.attitude[0])
            * 180.0
            / math.pi,
            10,
        ) % 360.0

    def penup(self):
        logging.info("simulating pen UP")
        self.state.penup()
        return self

    def pendown(self):
        logging.info("simulating pen DOWN")
        self.state.pendown()
        return self

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self.state.home()
        return self

    # No bye, no deletion, python garbage collect...

