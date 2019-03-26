import time

import functle


def triangle():
    dist = 200

    # we use with as a guarantee to cleanup our resource :
    # our delegate implementation, outside of our functional design.
    with functle.functle() as (impl, state, compose):

        # adhoc function composition in python
        functle.move(
            dist,
            functle.left(
                120, functle.move(dist, functle.left(120, functle.move(dist, state)))
            ),
        )

        # Can also be written somewhat a bit differently with currying :

        # Planning the triangle
        trngl = functle.move(dist)(
            functle.left(120)(
                functle.move(dist)(functle.left(120)(functle.move(dist)))
            )
        )

        # TODO : change color to make it obvious ?

        # actually running it
        trngl(state)

        # Or even nicer with composition handle separately,
        # And still leveraging currying

        # Planning the triangle
        trngl = compose(
            functle.move(dist),
                        functle.left(120),
                        functle.move(dist),
                        functle.left(120),
                        functle.move(dist),
        )

        # TODO : change color to make it obvious ?

        # actually running it
        trngl(state)


if __name__ == "__main__":
    triangle()
    time.sleep(5)  # hack to have the time to see something...
