import uuid
from typing import Optional, Union

from ..predicates import *
from ..matcher import CheckOperator


def numberlike(value):
    # string like num, int, decimal

    try:
        float(value)
        return True
    except ValueError:
        return False


def test_matchy_types():
    assert IsType(str).match("arst")
    assert not IsType(str).match(123)

    # assert CheckOperator.match_item('a', 'b')        # should we handle literals?

    assert CheckOperator.match_item('a', Is('a'))
    assert CheckOperator.match_item('a', Is())
    assert CheckOperator.match_item(None, Is())
    assert not CheckOperator.match_item('b', Is('a'))
    assert CheckOperator.match_item({'a', 'b'}, Is({'a', 'b'}))

    assert CheckOperator.match_item(None, IsType(Any))
    assert CheckOperator.match_item({1, 2, 4}, IsType(Any))

    assert CheckOperator.match_item('a', IsType(str))
    assert CheckOperator.match_item(888, IsType(int))
    assert not CheckOperator.match_item(888, IsType(str))

    # with pytest.raises(Exception):
    #     CheckOperator.match_item(888, MatchType("foo"))

    assert CheckOperator.match_item(2, IsType(Optional[int]))
    assert CheckOperator.match_item(None, IsType(Optional[int]))

    # if python >= 3.10, you can use simplified union syntax (PEP 604)
    assert CheckOperator.match_item(2, IsType(str | int))
    assert CheckOperator.match_item('word', IsType(str | int))
    assert not CheckOperator.match_item(None, IsType(str | int))

    # this does not work because of old 2.x typeguard version (I think fixed in 3.0)
    # assert not CheckOperator.match_item(None, MatchType(str | int))


def test_matchy_type_like():
    assert CheckOperator.match_item(2, IsTypeLike(float))
    assert CheckOperator.match_item(2.12, IsTypeLike(float))
    assert CheckOperator.match_item("2.5", IsTypeLike(float))
    assert not CheckOperator.match_item("word", IsTypeLike(float))

    uid = uuid.uuid4()

    assert CheckOperator.match_item(uid, IsTypeLike(uuid.UUID))
    assert CheckOperator.match_item(str(uid), IsTypeLike(uuid.UUID))
    assert not CheckOperator.match_item(123, IsTypeLike(uuid.UUID))


def test_matchy_functions():
    assert CheckOperator.match_item(3, IsEval(lambda x: 0 < x < 10))
    assert not CheckOperator.match_item(34, IsEval(lambda x: 0 < x < 10))

    assert CheckOperator.match_item(3, IsEval(numberlike))
    assert CheckOperator.match_item(3.52, IsEval(numberlike))
    assert CheckOperator.match_item('-12.8', IsEval(numberlike))
    assert not CheckOperator.match_item(None, IsEval(numberlike))
    assert not CheckOperator.match_item("word", IsEval(numberlike))


def test_match_multi_matcher():
    assert CheckOperator.match_item(5, IsEval(
        lambda x: IsType(int).match(x)))

    # joining a match function with a match type
    assert CheckOperator.match_item(7, IsEval(
        lambda x: IsType(int).match(x) and (1 < x < 10)))

    assert not CheckOperator.match_item(7, IsEval(
        lambda x: IsType(int).match(x) and (1 < x < 5)))

    assert not CheckOperator.match_item(7, IsEval(
        lambda x: IsType(str).match(x) and (1 < x < 10)))


def test_matchy_eval():
    assert CheckOperator.match_item(2, "~MM~ IsType(int)")
    assert not CheckOperator.match_item(2, "~MM~IsType(str) ")
