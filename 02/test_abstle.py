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
        cls.a = abstle.create(cls.mock_turtle)

        assert cls.mock_turtle.position.called
        assert cls.mock_turtle.heading.called
        assert cls.mock_turtle.pen.called

    def test_move(self):
        """ Testing one value of distance"""
        abstle.move(200, self.a)
        assert self.mock_turtle.forward.called

    def test_right(self):
        """ Testing one value of right angle"""
        abstle.right(42, self.a)
        assert self.mock_turtle.right.called

    def test_left(self):
        """ Testing one values of left angle"""
        abstle.left(42, self.a)
        assert self.mock_turtle.left.called

    def test_penup(self):
        """Testing that penup actually put the pen up"""
        abstle.penup(self.a)
        assert self.mock_turtle.penup.called

    def test_pendown(self):
        """Testing that pendown actually put the pen down"""
        abstle.pendown(self.a)
        assert self.mock_turtle.pendown.called


if __name__ == "__main__":
    unittest.main()
