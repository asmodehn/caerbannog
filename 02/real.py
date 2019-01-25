import logging
import turtle
from sim import SimTurtle

# The composed (delegation) OO architecture
# Taking SimTurtle turtle.Turtle as an unknown black box
# => we do not know, so we simulate, based on hypothesis, and we experiment to confirm/infirm them.
class InteractiveTurtle:

    model = SimTurtle()
    view = turtle.Turtle()

    # abasic comparison function to make sure our model stays on track...
    def _compare_model(self):
        assert (
            self.model.position == self.position()
        ), f"Model position {self.model.position} inconsistent with reality : {self.position()}"
        assert (
            self.model.heading() == self.heading()
        ), f"Model angle {self.model.heading()} inconsistent with reality : {self.heading()}"

    def position(self):
        # Apparently we should use here the "real" one (from the view)
        return self.view.position()

    def heading(self):
        # Apparently we should use here the "real" one (from the view)
        return self.view.heading()

    def move(self, distance: int):

        # TMP HACK
        distance = int(distance)

        logging.info("move {0}".format(distance))
        self._compare_model()

        self.model.move(distance)
        self.view.forward(distance=distance)

        self._compare_model()

    def right(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree right".format(angle))
        self._compare_model()

        self.model.turn(angle * -1)
        # Note here that with just a minor difference in interface, errors can creep in.
        # This actually means a different model would have been a better fit for our actual implementation.
        self.view.right(angle)

        self._compare_model()

    def left(self, angle: int):

        # TMP HACK
        angle = int(angle)

        logging.info("turn {0} degree left".format(angle))
        self._compare_model()

        self.model.turn(angle)
        self.view.left(angle)

        self._compare_model()

    def penup(self):
        logging.info("pen UP")
        # Not asserting : for later visual comparison only
        self.model.penup()
        self.view.penup()

    def pendown(self):
        logging.info("pen DOWN")
        # Not asserting : for later visual comparison only
        self.model.pendown()
        self.view.pendown()

    def home(self):
        logging.info("going home")
        self._compare_model()

        self.model.home()
        self.view.home()

        self._compare_model()

    def reset(self):
        logging.info("RESET!")
        self._compare_model()

        self.model = SimTurtle()
        self.view.reset()

        self._compare_model()

    def bye(self):
        logging.info("BYE!")
        self.view.getscreen().bye()