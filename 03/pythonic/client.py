import time

import functle


def triangle():
    state = functle.Functle()
    dist = 200

    # fluent pythonic function composition in python
    state.move(dist).left(120).move(dist).left(120).move(dist)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
