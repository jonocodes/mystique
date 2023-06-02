from typing import Any

from beartype.door import is_bearable


class Is:

    def __init__(self, query=Any):
        self.query = query

    def match(self, value):
        # this is equivalent to MatchType(Any|None)
        if self.query is Any:
            return True

        # if they set a value, do a value match
        # Probably best to not use this as it is slower than literal matching,
        #   but there are some cases where it can make sense.
        return self.query == value


class IsEnum(Is):
    def match(self, value):
        pass  # TODO


class IsType(Is):

    def match(self, value):
        return is_bearable(value, self.query)


class IsTypeLike(Is):

    def match(self, value):
        # only takes a single type (no generics or optionals)
        try:
            converted = self.query(str(value))
        except ValueError:
            return False

        return is_bearable(converted, self.query)


class IsEval(Is):

    def match(self, value):
        try:
            return self.query(value)
        except Exception:
            return False
