import time

import tootle


def triangle():
    with tootle.TurtleState() as do:

        dist = 200

        moved = do(tootle.move, dist)
        if moved < dist:
            print("error")
        else:
            do(tootle.left, 120)
            do(tootle.move, dist)
            do(tootle.left, 120)
            do(tootle.move, dist)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
