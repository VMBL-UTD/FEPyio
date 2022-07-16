import json
from collections.abc import Sized
from typing import OrderedDict


def prune_dict(d: dict, *, prune_empty_iterables: bool = False) -> dict:
    """Return a new dictionary without keys for 'None' values.

    If prune_empty_iterables=True, iterables of length 0 will be pruned as well.
    """
    if prune_empty_iterables:
        return {
            key: value
            for (key, value) in d.items()
            if value is not None and (not isinstance(value, Sized) or len(value) > 0)
        }
    return {key: value for (key, value) in d.items() if value is not None}


def prune_dict_inplace(d: dict) -> None:
    """Remove keys in dictionary for 'None' values in place."""
    for key in d:
        if d[key] is None:
            del d[key]


def unlist_dict(d: dict) -> dict:
    """Replace any single item list values with the single item. Return new dict."""
    _dict = {}

    for (key, value) in d.items():
        # Left as 'if' tree for possible expansion
        # If value is a list of length 1, use the first element as the value
        _value = value[0] if isinstance(value, list) and len(value) == 1 else value
        _dict[key] = _value

    return _dict


def to_dict(od: OrderedDict):
    """Convert a nested OrderedDict to a dict. Only works on json serializable objects.

    See: https://stackoverflow.com/a/27373073/
    """
    return json.loads(json.dumps(od))
