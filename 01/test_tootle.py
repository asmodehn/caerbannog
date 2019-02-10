import unittest
import random



import tootle


class TestTootle(unittest.TestCase):

    def setUp(self):
        self.t = tootle.Tootle()
        # Finding the maximum distance we can move, in one direction, without reaching the edge.
        self.max_test_dist = min(self.t.getscreen().canvwidth, self.t.getscreen().canvheight)
        self.max_test_angle = 360

    def check_move(self, dist: int):
        """
        Implements one check of move
        :param dist: the distance to move
        :return:
        """
        # get position before
        p0 = self.t.position
        self.t.move(dist)

        # get position after
        p1 = self.t.position

        assert p1 - p0 == dist

    def test_move(self):
        """ Testing multiple values of distance"""
        for d in [random.randint(0, self.max_test_dist) for _ in range(20)]:
            self.check_move(d)

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
