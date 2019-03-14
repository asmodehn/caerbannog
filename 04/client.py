import time

import montle


def triangle():
    # planning for triangle
    dist = 2000

    # we use with as a guarantee to cleanup our resource :
    # our delegate implementation, outside of our functional design.
    with montle.montle() as impl:

        impl, actual_dist = montle.move(dist)(impl)

        if actual_dist < dist:
            # attempt smaller triangle
            dist = actual_dist
        else:
            pass  # TODO : same logic as in video example

        # Note we can compose actions like functions
        impl, actual_dist = montle.move(dist)(montle.left(120)(impl))

        if actual_dist < dist:
            # blah
            pass
        else:
            # blah
            pass

        impl, actual_dist = montle.move(dist)(montle.left(120)(impl))

        if actual_dist < dist:
            # blah
            pass
        else:
            # blah
            pass


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
