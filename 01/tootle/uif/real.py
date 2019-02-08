import turtle
import logging


# The usual OO inheritance interface
# taking turtle.Turtle as an unknown black box
# => we do not know, so we simulate, based on hypothesis, and we experiment to confirm/infirm them.
class InteractiveTurtle(turtle.Turtle):

    def __init__(self, simulation):
        self.model = simulation
        super().__init__()

    # a basic comparison function to make sure our model stays on track...
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

    def reset(self, simulation):
        logging.info("RESET!")
        self._compare_model()

        self.model = simulation
        super().reset()

        self._compare_model()

    def bye(self):
        logging.info("BYE!")
        super().getscreen().bye()
