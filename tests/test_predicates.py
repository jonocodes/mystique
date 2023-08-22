import uuid
from typing import Optional, Union

from ..src.predicates import *
from ..src.matcher import CheckOperator


check = CheckOperator.match_item


def numberlike(value):
    # string like num, int, decimal

    try:
        float(value)
        return True
    except ValueError:
        return False


def test_match_types():
    assert IsType(str).match("arst")
    assert not IsType(str).match(123)

    # assert check('a', 'b')        # should we handle literals?

    assert check('a', Is('a'))
    assert check('a', Is())
    assert check(None, Is())
    assert not check('b', Is('a'))
    assert check({'a', 'b'}, Is({'a', 'b'}))

    assert check(None, IsType(Any))
    assert check({1, 2, 4}, IsType(Any))

    assert check('a', IsType(str))
    assert check(888, IsType(int))
    assert not check(888, IsType(str))

    # with pytest.raises(Exception):
    #     check(888, MatchType("foo"))

    assert check(2, IsType(Optional[int]))
    assert check(None, IsType(Optional[int]))

    # if python >= 3.10, you can use simplified union syntax (PEP 604)
    assert check(2, IsType(str | int))
    assert check('word', IsType(str | int))
    assert not check(None, IsType(str | int))

    # this does not work because of old 2.x typeguard version (I think fixed in 3.0)
    # assert not check(None, MatchType(str | int))


def test_match_type_like():
    assert check(2, IsTypeLike(float))
    assert check(2.12, IsTypeLike(float))
    assert check("2.5", IsTypeLike(float))
    assert not check("word", IsTypeLike(float))

    uid = uuid.uuid4()

    assert check(uid, IsTypeLike(uuid.UUID))
    assert check(str(uid), IsTypeLike(uuid.UUID))
    assert not check(123, IsTypeLike(uuid.UUID))


def test_match_functions():
    assert check(3, IsEval(lambda x: 0 < x < 10))
    assert not check(34, IsEval(lambda x: 0 < x < 10))

    assert check(3, IsEval(numberlike))
    assert check(3.52, IsEval(numberlike))
    assert check('-12.8', IsEval(numberlike))
    assert not check(None, IsEval(numberlike))
    assert not check("word", IsEval(numberlike))


def test_match_multi_matcher():
    assert check(5, IsEval(
        lambda x: IsType(int).match(x)))

    # joining a match function with a match type
    assert check(7, IsEval(
        lambda x: IsType(int).match(x) and (1 < x < 10)))

    assert not check(7, IsEval(
        lambda x: IsType(int).match(x) and (1 < x < 5)))

    assert not check(7, IsEval(
        lambda x: IsType(str).match(x) and (1 < x < 10)))


def test_match_parsed():
    assert check(2, "~MM~ IsType(int)")
    assert not check(2, "~MM~IsType(str) ")
