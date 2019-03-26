import pytest
import functle




def test_compose_unit():
    # TODO : more complete and corner-cased testing

    add2 = lambda x: (2 + x)
    assert functle.compose(3) == 3 == functle.compose()(3)



def test_compose():
    # TODO : more complete and corner-cased testing

    add2 = lambda x: (2 + x)
    assert functle.compose(add2, add2, add2)(3) == 9


def test_compose_compose():
    # TODO : more complete and corner-cased testing
    add2 = lambda x: (2 + x)
    add3 = lambda x: (3 + x)

    assert functle.compose(functle.compose(add2, add2), add3)(3) == 10


# TODO : proper testing on application monoid properties/laws for compose...


if __name__ == "__main__":
    pytest.main()