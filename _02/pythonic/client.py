import time

import abstle


def triangle():
    abstle = abstle.Abstle()
    dist = 200

    # as a result of encapsulating the state in a class with methods
    # we do not need to manage the state here
    abstle.move(dist)
    abstle.left(120)
    abstle.move(dist)
    abstle.left(120)
    abstle.move(dist)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
