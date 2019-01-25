import turtle
import logging

from utils import PenState


# Directly, naively, modeled in python 3.6
# from the code shown in : https://www.youtube.com/watch?v=AG3KuqDbmhM



# Code isolated from the side-effects (commands and display)
# Made to look as close as possible from code presented in Scott Wlaschin's NDC talk
# Additionally is serves us as a simulation without relying on any side effects.
#
# note that doing so we already, in a way, separated the "model" from the actual "implementation code".
# We reuse here turtle.Vec2D to get exactly the same code representing the model, and what is actually happening.
class TurtleState:

    currentPosition = turtle.Vec2D(0, 0)
    currentAttitude = turtle.Vec2D(1, 0)  # Represents an angle in a nice computable way
    currentPenState = PenState.DOWN

    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        self.currentPosition = self.currentPosition + distance * self.currentAttitude

    def turn(self, angle: int):
        logging.info("simulating turn {0} degree".format(angle))

        self.currentAttitude = self.currentAttitude.rotate(angle)

    def penup(self):
        logging.info("simulating pen UP")
        self.currentPenState = PenState.UP

    def pendown(self):
        logging.info("simulating pen DOWN")
        self.currentPenState = PenState.DOWN

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        logging.info("simulating going home")
        self.currentPosition = turtle.Vec2D(0, 0)
        self.currentAttitude = turtle.Vec2D(1, 0)
