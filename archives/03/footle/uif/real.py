import turtle

from ..sim import SimTurtle


# The "functional" architecture ( from the talk )
# taking turtle.Turtle as an unknown black box
# => we do not know, so we simulate, based on hypothesis, and we experiment to confirm/infirm them.
import logging


class InteractiveTurtle:

    model = SimTurtle()
    real = turtle.Turtle()

    # a basic comparison function to make sure our model stays on track...
    # Also called permanent live testing / Zero Assumptions Programming
    def _compare_model(self):
        assert (
            self.model.position == self.position()
        ), f"Model position {self.model.position} inconsistent with reality : {self.position()}"
        assert (
            self.model.heading(self.model.state) == self.heading()
        ), f"Model angle {self.model.heading(self.model.state)} inconsistent with reality : {self.heading()}"

    def position(self):
        # Apparently we should use here the "real" one
        return self.real.position()

    def heading(self):
        # Apparently we should use here the "real" one
        return self.real.heading()

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        logging.info("move {0}".format(distance))
        self._compare_model()

        self.model.move(distance)
        self.real.forward(distance=distance)

        self._compare_model()
        return self

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree right".format(angle))
        self._compare_model()

        self.model.turn(angle * -1)
        # Note here that with just a minor difference in interface, errors can creep in.
        # This actually means a different model would have been a better fit for our actual implementation.
        self.real.right(angle)

        self._compare_model()
        return self

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree left".format(angle))
        self._compare_model()

        self.model.turn(angle)
        self.real.left(angle)

        self._compare_model()
        return self

    def penup(self):
        logging.info("pen UP")
        # Not asserting : for later visual comparison only
        self.model.penup()
        self.real.penup()
        return self

    def pendown(self):
        logging.info("pen DOWN")
        # Not asserting : for later visual comparison only
        self.model.pendown()
        self.real.pendown()
        return self

    def home(self):
        logging.info("going home")
        self._compare_model()

        self.model.home()
        self.real.home()

        self._compare_model()
        return self

    def reset(self):
        logging.info("RESET!")
        self._compare_model()

        self.model = SimTurtle()
        self.real.reset()

        self._compare_model()
        return self

    def bye(self):
        logging.info("BYE!")
        self.real.getscreen().bye()
        # no return, nothing after.

