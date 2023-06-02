from pprint import pprint

from deepdiff import DeepDiff
from deepdiff.operator import BaseOperator

from .predicates import *

STR_PREFIX = '~MM~'


class CheckOperator(BaseOperator):

    @staticmethod
    def match_item(t1, t2):
        if isinstance(t2, Is):
            return t2.match(t1)

        if isinstance(t2, str) and t2.startswith(STR_PREFIX):
            exp = t2[4:].strip()
            matcher = eval(exp)
            if isinstance(matcher, Is):
                return matcher.match(t1)

        return None

    # TODO: figure out why these are both needed together

    def match(self, level) -> bool:
        result = self.match_item(level.t1, level.t2)
        if result is not None:
            return result
        return super().match(level)

    def give_up_diffing(self, level, diff_instance):
        result = self.match_item(level.t1, level.t2)
        if result is not None:
            return result


class Matcher:

    def __init__(self, sparse_dicts=False):
        self.sparse_dicts = sparse_dicts

    def matches(self, original, matcher):
        diff = DeepDiff(original, matcher, custom_operators=[CheckOperator()],
                        verbose_level=2)

        if self.sparse_dicts:
            diff.pop('dictionary_item_removed', None)

        if diff == {}:
            return True

        # TODO: print nicer into pytest error message
        pprint(diff)

        return False
