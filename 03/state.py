from utils import PenState



# Code isolated from the side-effects (commands and display)
# Made to look as close as possible from code presented in Scott Wlaschin's NDC talk
# Additionally is serves us as a simulation without relying on any side effects.
#
# note that doing so we already, in a way, separated the "model" from the actual "implementation code".
# We reuse here turtle.Vec2D to get exactly the same code representing the model, and what is actually happening.
import turtle


class TurtleState:

    # Immutable state
    state = (turtle.Vec2D(0, 0), turtle.Vec2D(1, 0), PenState.DOWN)

    @property
    def position(self):
        return self.state[0]

    @property
    def attitude(self):
        return self.state[1]

    @property
    def penState(self):
        return self.state[2]

    # Note : using self is how we pass the state(=instance) around in python !
    def move(self, distance: int):
        endPosition = self.position + distance * self.attitude

        # mutating the state(=instance)
        self.state = (endPosition, self.attitude, self.penState)
        return self

    def turn(self, angle: int):
        # mutating the state(=instance)
        self.state = (self.position, self.attitude.rotate(angle), self.penState)
        return self

    def penup(self):
        # mutating the state(=instance)
        self.state = (self.position, self.attitude, PenState.UP)
        return self

    def pendown(self):
        # mutating the state(=instance)
        self.state = (self.position, self.attitude, PenState.DOWN)
        return self

    # Adding these to complete the model with a minimum of useful functions
    def home(self):
        # mutating the state(=instance)
        self.state = (turtle.Vec2D(0, 0), turtle.Vec2D(1, 0), self.penState)
        return self
