from dataclasses import dataclass
from enum import auto, Enum

from ..matcher import Matcher
from ..predicates import *


class Color(Enum):
    red = auto()
    green = auto()
    blue = auto()


@dataclass
class Car:
    make: str
    model: str
    year: int
    color: Color



def test_objects():
    data = Car('Prius', 'V', 2014, Color.red)

    matcher = Car('Prius', 'V', IsType(int), IsType(Color))

    assert Matcher().matches(data, matcher)

    matcher = Car('Prius', 'V', IsType(str), IsType(Color))

    assert not Matcher().matches(data, matcher)


def test_deep():
    m = Matcher()

    # list with dict
    data = ['x', 'y', 2, [2, 4, 5], {'a': 1, 'b': "111"}]
    matcher = ['x', IsType(str), IsType(int | None), IsType(list[int]),
                    IsType(Any)]

    assert m.matches(data, matcher)

    # dict with obj
    data = {'a': 1, 'b': "111", 
        "c": Car('Prius', 'V', 2014, Color.red),
        "d": Car('Prius', 'V', 2018, Color.red)}

    matcher = {'a': 1, 'b': "111", "c": IsType(Car), "d": IsType(Any)}

    assert m.matches(data, matcher)

    # obj in obj
    matcher = {'a': 1, 'b': "111", "c": IsType(Car), "d": Car('Prius', 'V', IsType(int), IsType(Color))}

    assert m.matches(data, matcher)

    matcher = {'a': 1, 'b': "111", "c": IsType(Car), "d": Car('Prius', 'V', IsType(str), Is(Color.red))}

    assert not m.matches(data, matcher)


def test_sparse_dicts():
    data = {'a': 1, 'b': 2, 'c': 3}
    match_expression = {'a': 1}

    m = Matcher(sparse_dicts=True)

    assert m.matches(data, match_expression)

    data = {'a': 1, 'b': 2, 'c': 3}
    match_expression = {'a': 1, 'd': 4}

    assert not m.matches(data, match_expression)

    data = [1, 2, 3]
    match_expression = [1, 2]

    assert not m.matches(data, match_expression)
