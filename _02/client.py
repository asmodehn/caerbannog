import time

import tootle


def triangle():
    state = tootle.create()
    dist = 200

    tootle.move(dist, state)
    tootle.left(120, state)
    tootle.move(dist, state)
    tootle.left(120, state)
    tootle.move(dist, state)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
