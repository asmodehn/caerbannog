import time

import tootle


def triangle():

    with tootle.MonadicTurtle() as m:

        dist = 20000
        moved = m.move(dist)

        if moved() < dist:
            print(f"error {moved} instead of {dist}")
        else:
            m.left(120)
            m.move(dist)
            m.left(120)
            m.move(dist)

    # Exiting the with block actually run the monad actions


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
