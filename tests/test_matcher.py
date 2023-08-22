import json
from dataclasses import dataclass
from enum import auto, Enum

from ..src.matcher import Matcher
from ..src.predicates import *


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


def test_json_string():

    # sometimes you may have an external json file perhaps where you cant inject python expressions into it for matching. So we interpret strings as matchers.

    data = {'foo': 'baz', 'bar': [1, 3]}
    
    with open('tests/matcher1.json', 'r') as jf:
        match_expression = json.load(jf)
        print(match_expression)

    assert Matcher().matches(data, match_expression)


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


def test_examples():
    # these can be copied into the readme

    data = {'foo': 'baz', 'bar': [1, 3]}

    # exact match
    assert Matcher().matches(data, {'foo': 'baz', 'bar': [1, 3]})

    # make sure one of the values just matches a type, instead of a value
    assert Matcher().matches(data, {'foo': 'baz', 'bar': IsType(list[int])})

    # perhaps you don't care about the type at all. just that there is a value
    assert Matcher().matches(data, {'foo': 'baz', 'bar': Is()})

    # check anything you want by writing your own logic
    assert Matcher().matches(data, {'foo': 'baz', 'bar': IsEval(
        lambda x: len(x) == 2)})

    # if you dont care if a key is present or not, use 'sparse_dicts' settinvg
    assert Matcher(sparse_dicts=True).matches(data, {'foo': 'baz'})