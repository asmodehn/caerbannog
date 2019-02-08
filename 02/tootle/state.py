import turtle
import logging
from .utils import PenState


# Code isolated from the side-effects (commands and display)
# Made to look as close as possible from code presented in Scott Wlaschin's NDC talk
# Additionally is serves us as a simulation without relying on any side effects.
#
# note that doing so we already, in a way, separated the "model" from the actual "implementation code".
# We reuse here turtle.Vec2D to get exactly the same code representing the model, and what is actually happening.

class TurtleState:
    _position = turtle.Vec2D(0, 0)
    _attitude = turtle.Vec2D(1, 0)
    _penState = PenState.DOWN

    # Read-only state
    @property
    def position(self):
        return self._position

    @property
    def attitude(self):
        return self._attitude

    @property
    def penState(self):
        return self._penState

    # Note : using self is how we pass the state(=instance) around in python !
    def move(self, distance: int):
        endPosition = self.position + distance * self.attitude

        # mutating the state(=instance)
        self._position = endPosition

    def turn(self, angle: int):

        # mutating the state(=instance)
        self._attitude = self.attitude.rotate(angle)

    def penup(self):
        logging.info("simulating pen UP")
        self._penState=PenState.UP

    def pendown(self):
        logging.info("simulating pen DOWN")
        self._penState=PenState.DOWN

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self._position=turtle.Vec2D(0, 0)
        self._attitude=turtle.Vec2D(1, 0)
