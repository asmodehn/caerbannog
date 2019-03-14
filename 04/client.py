import time

import montle


def triangle():
    # planning for triangle
    dist = 200

    Mtriangle = montle.move(dist)


    # adhoc function composition in python
    # Mtriangle = montle.move(dist,
    #                          montle.left(120,
    #                               montle.move(dist,
    #                                            montle.left(120,
    #                                                         montle.move(dist)))))

    # we use with as a guarantee to cleanup our resource :
    # our delegate implementation, outside of our functional design.
    with montle.montle() as impl:
        Mtriangle(impl)


if __name__ == '__main__':
    triangle()
    time.sleep(5)  # hack to have the time to see something...
