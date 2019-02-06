import time

import tootle


def triangle():
    state = tootle.TurtleState()
    dist = 200

    tootle.move(dist,
                tootle.left(120,
                            tootle.move(dist,
                                        tootle.left(120,
                                                    tootle.move(dist,
                                                                state)))))


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
