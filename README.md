# Mystique

A loose data matcher to help you write Python tests

# Introduction

Imagine you need to fetch some data from a JSON API in a test. It returns a payload with 10 fields, but you only care about two of them. With Mystique you can be as rigerous or loose as you want when checking data equivalence. Check against any combination of dictionaries, lists, and objects.

# Examples

```python
from matcher import Matcher
from matcher.predicates import Is, IsEval, IsType

data = {'foo': 'baz', 'bar': [1, 3]}

# exact match
assert Matcher().matches(data,
    {'foo': 'baz', 'bar': [1, 3]})

# make sure one of the values just matches a type, instead of a value
assert Matcher().matches(data,
    {'foo': 'baz', 'bar': IsType(list[int])})

# perhaps you don't care about the type at all. just that there is a value
assert Matcher().matches(data,
    {'foo': 'baz', 'bar': Is()})

# check anything you want by writing your own logic
assert Matcher().matches(data,
    {'foo': 'baz', 'bar': IsEval(lambda x: len(x) == 2)})

# if you dont care if a key is present or not, use 'sparse_dicts' settinvg
assert Matcher(sparse_dicts=True).matches(data, {'foo': 'baz'})
```

See tests/ for more examples.

# Requirements

- python >= 3.7
- python >= 3.10 recommended

# Development

```bash
make setup

make test
```
