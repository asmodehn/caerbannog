import math
import logging

from utils import PenState
from State import TurtleState


class SimTurtle(TurtleState):

    #: the list of lines drawn, as the expected side effect.
    drawing = []

    # no init, just like in the code model

    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        old_position = self.currentPosition
        super().move(distance)

        if self.currentPenState == PenState.DOWN:
            self.drawing.append((old_position, self.currentPosition))

    def heading(self):
        # From https://github.com/python/cpython/blob/master/Lib/turtle.py#L1895
        return round(
            math.atan2(self.currentAttitude[1], self.currentAttitude[0])
            * 180.0
            / math.pi,
            10,
        ) % 360.0

    # No bye, no deletion, python garbage collect...
