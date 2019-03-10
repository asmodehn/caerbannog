import unittest
import unittest.mock as mock
import random

# for mocking
import turtle

# for testing
import tootle


class TestTootle(unittest.TestCase):
    """
    It is overly complicated to test the actual Turtle behavior with the current OO design,
    since the inheritance mechanism uses the logic of the super class and related class hierarchies.
    Also any action with side effect will modify the environment, which we don't control by definition,
    by changing the start position of the turtle and will affect the following test, for example.

    What we can do however, is that our own code is using the rest of the code as expected, using a mock.
    The mock will prevent any side effect by intercepting any procedure call, and register counters,
    before it interferes with the outside world. but we need to investigate the superclass hierarchy to understand
    its behavior and relationship.This breaks the original encapsulation intent...

    Anyway, it is better than not testing, but this tests almost nothing.
    It will not test the whole behavior, and it doesn't scale to test integration of multiple components.
    It is also quite fragile with inheritance, as we have to plug our mock in the exact place, which can be quite hacky
    """

    @mock.patch('turtle.TurtleScreen', autospec=True)
    def setUp(self, mock_tscreen):
        self.t = tootle.Tootle()
        # TODO ... currently mock breaks the turtle...
        assert mock_tscreen.called_with()

    def check_move(self, dist: int):
        """
        Implements one check of move
        :param dist: the distance to move
        :return:
        """
        # get position before
        p0 = self.t.position

        # get position after
        p1 = self.t.position

        assert p1 - p0 == dist

    @mock.patch("turtle.Turtle.forward")
    def test_move(self, mockturtle):
        """ Testing multiple values of distance"""
        for d in [random.randint(0, self.max_test_dist) for _ in range(20)]:
            self.t.move(d)
            assert mockturtle.forward.assert_called_with(d)

    def check_right(self, angle: int):
        """Testing that right actually orientates right"""

        # get angle before
        o1 = self.t.angle

        self.t.right(angle)

        o2 = self.t.angle
        #assert o1 + angle == o2
        assert o2 - o1 == 360 - o2

    def test_right(self):
        """ Testing multiple values of distance"""
        for a in [random.randint(0, self.max_test_angle) for _ in range(20)]:
            self.check_right(a)

    def check_left(self, angle: int):
        """Testing that left actually orientates left"""

        # get angle before
        o1 = self.t.angle

        self.t.left(angle)

        o2 = self.t.angle
        assert o2 - o1 == angle

    def test_left(self):
        """ Testing multiple values of distance"""
        for a in [random.randint(0, self.max_test_angle) for _ in range(20)]:
            self.check_right(a)

    def test_penup(self):
        """Testing that penup actually put the pen up"""
        self.t.penup()

        ps1 = self.t.pen
        assert ps1 == tootle.PenState.UP

    def test_pendown(self):
        """Testing that pendown actually put the pen down"""
        self.t.pendown()

        ps1 = self.t.pen
        assert ps1 == tootle.PenState.DOWN


if __name__ == '__main__':
    unittest.main()
