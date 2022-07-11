def prune_dict(d: dict) -> dict:
    """Return a new dictionary without keys for 'None' values."""
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
