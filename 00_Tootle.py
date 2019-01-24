import math
import turtle
import cmd
import enum
import logging


# Directly, naively, modeled in python 3.6
# from the code shown in : https://www.youtube.com/watch?v=AG3KuqDbmhM

# Side Note: Yes, Python has enums !
class PenState(enum.Enum):
    UP = -1
    DOWN = 1


# Code isolated from the side-effects (commands and display)
# Made to look as close as possible from code presented in Scott Wlaschin's NDC talk
# Additionally is serves us as a simulation without relying on any side effects.
#
# note that doing so we already, in a way, separated the "model" from the actual "implementation code".
# We reuse here turtle.Vec2D to get exactly the same code representing the model, and what is actually happening.
class SimTurtle:

    currentPosition = turtle.Vec2D(0, 0)
    currentAttitude = turtle.Vec2D(1, 0)  # Represents an angle in a nice computable way
    currentPenState = PenState.DOWN
    #: the list of lines drawn, as the expected side effect.
    drawing = []

    # no init, just like in the code model

    def move(self, distance: int):
        logging.info("simulating move {0}".format(distance))

        endPosition = self.currentPosition + distance * self.currentAttitude

        if self.currentPenState == PenState.DOWN:
            self.drawing.append((self.currentPosition, endPosition))

        self.currentPosition = endPosition

    def turn(self, angle: int):
        logging.info("simulating turn {0} degree".format(angle))

        self.currentAttitude = self.currentAttitude.rotate(angle)

    def heading(self):
        # From https://github.com/python/cpython/blob/master/Lib/turtle.py#L1895
        return round(
            math.atan2(self.currentAttitude[1], self.currentAttitude[0])
            * 180.0
            / math.pi,
            10,
        ) % 360.0

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

    # No bye, no deletion, python garbage collect...


# The usual OO inheritance interface
# taking turtle.Turtle as an unknown black box
# => we do not know, so we simulate, based on hypothesis, and we experiment to confirm/infirm them.
class InteractiveTurtle(turtle.Turtle):

    model = SimTurtle()

    # abasic comparison function to make sure our model stays on track...
    def _compare_model(self):
        assert (
            self.model.currentPosition == self.position()
        ), f"Model position {self.model.currentPosition} inconsistent with reality : {self.position()}"
        assert (
            self.model.heading() == self.heading()
        ), f"Model angle {self.model.heading()} inconsistent with reality : {self.heading()}"

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        logging.info("move {0}".format(distance))
        self._compare_model()

        self.model.move(distance)
        super().forward(distance=distance)

        self._compare_model()

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree right".format(angle))
        self._compare_model()

        self.model.turn(angle * -1)
        # Note here that with just a minor difference in interface, errors can creep in.
        # This actually means a different model would have been a better fit for our actual implementation.
        super().right(angle)

        self._compare_model()

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree left".format(angle))
        self._compare_model()

        self.model.turn(angle)
        super().left(angle)

        self._compare_model()

    def penup(self):
        logging.info("pen UP")
        # Not asserting : for later visual comparison only
        self.model.penup()
        super().penup()

    def pendown(self):
        logging.info("pen DOWN")
        # Not asserting : for later visual comparison only
        self.model.pendown()
        super().pendown()

    def home(self):
        logging.info("going home")
        self._compare_model()

        self.model.home()
        super().home()

        self._compare_model()

    def reset(self):
        logging.info("RESET!")
        self._compare_model()

        self.model = SimTurtle()
        super().reset()

        self._compare_model()

    def bye(self):
        logging.info("BYE!")
        super().getscreen().bye()


# Usual cmd interface, OO-style
class TurtleRepl(cmd.Cmd):

    intro = "Welcome to the tootle shell.   Type help or ? to list commands.\n"
    prompt = "(tootle) "
    tootle = InteractiveTurtle()

    # ----- basic turtle commands -----
    def do_move(self, distance):
        "Move the turtle forward by the specified distance:  MOVE 10"
        self.tootle.move(distance)

    def do_left(self, angle):
        "Turn turtle right by given number of degrees:  LEFT 20"
        self.tootle.left(angle)

    def do_right(self, angle):
        "Turn turtle right by given number of degrees:  RIGHT 20"
        self.tootle.right(angle)

    def do_home(self, arg):
        "Return turtle to the home postion:  HOME"
        self.tootle.home()

    # This is "read-only"
    def do_position(self, arg):
        "Print the current turle position:  POSITION"
        print("Current position is {}".format(self.tootle.position()))

    # This is "read-only"
    def do_heading(self, arg):
        "Print the current turle heading in degrees:  HEADING"
        print("Current heading is {}".format(self.tootle.heading()))

    # This is only cosmetic :-)
    def do_color(self, arg = None):
        "Set the color:  COLOR BLUE"
        if arg is None or arg is '':
            arg = 'black'
        self.tootle.color(arg.lower())

    def do_reset(self, arg):
        "Clear the screen and return turtle to center:  RESET"
        self.do_color()
        self.tootle.reset()

    def do_bye(self, arg):
        "Stop recording, close the turtle window, and exit:  BYE"
        print("Thank you for using Turtle")
        self.tootle.bye()
        return True


if __name__ == "__main__":
    TurtleRepl().cmdloop()
