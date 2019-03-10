import unittest
import unittest.mock as mock
import random

import abstle


class TestTootle(unittest.TestCase):
    """
    With a functional interface, it is now much easier to inject our mock as a dependency.
    However it is still tricky to know what should happen when the class hierarchy is involved during creation.
    Also your test code still depends on the design of the code you want to test,
        which makes developing tests before hand a somewhat useless exercise.
    """

    @classmethod
    def setUpClass(cls):
        """
        Note this function is called only once per class instantiation.
        We then mock the used turtle.Turtle and we will check it s use when we call abstle functions
        :param self:
        :param mock_turtle:
        :return:
        """
        cls.mock_turtle = mock.MagicMock()
        cls.a = abstle.Abstle(cls.mock_turtle)

        # Using property decorator, we do not call position/heading/pen on creation/mutation anymore
        # Instead we will call only when the data is requested.
        assert not cls.mock_turtle.position.called
        assert not cls.mock_turtle.heading.called
        assert not cls.mock_turtle.pen.called

    def test_move(self):
        """ Testing one value of distance"""
        self.a.move(200)
        assert self.mock_turtle.forward.called

    def test_right(self):
        """ Testing one value of right angle"""
        self.a.right(42)
        assert self.mock_turtle.right.called

    def test_left(self):
        """ Testing one values of left angle"""
        self.a.left(42)
        assert self.mock_turtle.left.called

    def test_penup(self):
        """Testing that penup actually put the pen up"""
        self.a.penup()
        assert self.mock_turtle.penup.called

    def test_pendown(self):
        """Testing that pendown actually put the pen down"""
        self.a.pendown()
        assert self.mock_turtle.pendown.called


if __name__ == "__main__":
    unittest.main()
