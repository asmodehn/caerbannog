


import dataclasses


# TODO : we currently define it for only one argument.
# This can be extended to iterate on that argument, and be linked with itertools and others...





# Inspiration from returns: https://github.com/dry-python/returns/blob/master/returns/primitives/container.py

@dataclasses(frozen=True)
class Functor:



    def __call__(self, arg):

        # check identity morphism is preserved

        # check composition off morphisms is preserved

        return #TODO



class Applicative(Functor):
    pass

    # TODO


class Selective(Functor):




class Monad(Applicative):
