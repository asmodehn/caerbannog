import time

import tootle


def triangle():
    tt = tootle.Turtle()
    dist = 200

    tt.move(dist)
    tt.left(120)
    tt.move(dist)
    tt.left(120)
    tt.move(dist)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
