from __future__ import annotations

import random


class TypeSet:
    """
    It looks like a list, it behaves like a list, but it is not exactly a list
    => it cannot be empty ! We can always get the root (the origin list !) element

    It is also, like DSet, bimonadic in state:
    >>> three = typeset(1,2,3)  # return
    >>> three
    typeset(1, 2, 3)

    and join / duplicate are "implicit"

    >>> assert three == typeset(three)

    And bimonadic in time-dimension (for __call__ and __next__):

    # return is done via calling (appends to the list if already exists)
    >>> five1 = three(4)(5)
    >>> five2 = three(4,5)

    join/duplicate are "implicit" but rely on python semantics and feel like currying...
    >>> five1
    looperset(1, 2, 3, 4, 5)
    >>> five2
    looperset(1, 2, 3, 4, 5)

    extract is done via iterating (the usual stream comonad) in python
    >>> one_two_three = next(three)
    >>> one_two_three in [1, 2, 3]
    True

    It is also immutable which means if the result of a call is not stored, it will not persist.

    """
    def __init__(self, *elements):  # container / monadic interface
        """
        This builds a looperset. It is useful to note that this somewhat *changes* the usual *args semantics,
        as well as data behavior in python.
        :param elements: the elements of the frozen set
        """

        self.frozen = frozenset(elements)  # frozenset takes an iterable

    def __repr__(self):
        return f"typeset({', '.join(str(e) for e in self.frozen)})"  # attempting homoiconicity

    def __str__(self):
        return f"{{', '.join(str(e) for e in self.frozen)}}"  # pretty printing

    def __bool__(self):
        """ Falsy if empty, just like vector"""
        return bool(self.frozen)

    def __eq__(self, other: TypeSet):
        """ Strict equality - no duck typing here !
        """
        if type(self) != type(other):
            return False
        # exact same data in memory (optimization) or same content
        contentmatch = id(self.frozen) == id(other.frozen) or self.frozen == other.frozen
        return contentmatch

    def __call__(self, *elem) -> TypeSet:
        """ appending to the list """
        if len(elem) == 0:
            return self  # preventing duplication here
        return typeset(*self.frozen, *elem)

    def __contains__(self, item):
        """ Contains does not increment focus when checking whats inside ! Useful to check subtype..."""
        return item in self.frozen

    def __iter__(self):  # stream / comonadic interface
        return self

    def __next__(self):    # container (comonadic - state) interface: extract
        if self.frozen:
            return random.sample(self.frozen, 1)[0]
            # Returning one of the element
        else:
            return None  # TODO : probably need some clever trick here

    def __len__(self):
        return len(self.frozen) + 1

    # Algebra TODO


Void = TypeSet()


def typeset(*elems):
    if len(elems) == 0:
        return Void  # empty
    elif len(elems) == 1 and isinstance(elems[0], TypeSet):
        # To get a bimonad we need to encode an implicit join here so that we never need duplicate
        # even if we are semantically compatible.
        return TypeSet(*elems[0].frozen)
    else:
        return TypeSet(*elems)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
