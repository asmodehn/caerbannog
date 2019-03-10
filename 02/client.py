import time

import abstle


def triangle():
    state = abstle.create()
    dist = 200

    abstle.move(dist, state)
    abstle.left(120, state)
    abstle.move(dist, state)
    abstle.left(120, state)
    abstle.move(dist, state)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
