from dataclasses import dataclass

from ..matcher import Matcher
from ..predicates import *


@dataclass
class Car:
    make: str
    model: str
    year: int


def test_matchy_objects():
    obj_1 = Car('Prius', 'V', 2014)
    obj_matcher = Car('Prius', 'V', IsType(int))

    assert Matcher().matches(obj_1, obj_matcher)

    obj_matcher = Car('Prius', 'V', IsType(str))

    assert not Matcher().matches(obj_1, obj_matcher)


def test_matchy_deep():
    m = Matcher()

    # list with dict
    dict_1 = ['x', 'y', 2, [2, 4, 5], {'a': 1, 'b': "111"}]
    dict_matcher = ['x', IsType(str), IsType(int | None), IsType(list[int]),
                    IsType(Any)]

    assert m.matches(dict_1, dict_matcher)

    # dict with obj
    dict_2 = {'a': 1, 'b': "111", "c": Car('Prius', 'V', 2014), "d": Car('Prius', 'V', 2018)}

    matcher = {'a': 1, 'b': "111", "c": IsType(Car), "d": IsType(Any)}

    assert m.matches(dict_2, matcher)

    # obj in obj
    matcher = {'a': 1, 'b': "111", "c": IsType(Car), "d": Car('Prius', 'V', IsType(int))}

    assert m.matches(dict_2, matcher)

    matcher = {'a': 1, 'b': "111", "c": IsType(Car), "d": Car('Prius', 'V', IsType(str))}

    assert not m.matches(dict_2, matcher)


def test_matchy_partial():
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
